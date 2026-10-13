#!/usr/bin/env python3
"""Fit the Ağustos main theme to the length of a video.

The theme has three parts: an intro, a middle part that repeats, and an
outro. This script plays the intro, repeats the middle part in whole bars
for as long as the video needs, and then plays the outro. Silence fills the
last part of a bar, so the file has the exact length of the video.

Usage:
  python3 brand/audio/fit_theme.py SECONDS OUT.wav
  python3 brand/audio/fit_theme.py SECONDS OUT.wav --mix voice
  python3 brand/audio/fit_theme.py SECONDS OUT.wav --parts DIR

The parts are 16-bit PCM WAV files with the same rate and channels:
<parts>/<mix>/intro.wav, middle.wav and outro.wav. <parts>/theme.json
gives the number of bars in the middle part. README.md in this folder
tells how to make them. The script uses the Python standard library only.
"""

from __future__ import annotations

import argparse
import array
import json
import sys
import wave
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_PARTS = HERE / "main-theme"
JOIN_SECONDS = 0.01  # Each joint overlaps the two parts for 10 ms, so no joint clicks.


class ThemeError(Exception):
    """The parts or the length do not allow a fitted theme."""


@dataclass(frozen=True)
class Plan:
    middle_bars: int  # Bars of the middle part to play, over all repeats.
    pad: int          # Frames of silence after the outro.


def pieces(count: int, bars: int, edges: list[int]) -> list[int]:
    """Return the frame lengths of the middle pieces for `count` bars."""
    whole, rest = divmod(count, bars)
    return [edges[bars]] * whole + ([edges[rest]] if rest else [])


def length(intro: int, middle: list[int], outro: int, overlap: int) -> int:
    """Return the frames that `fit` writes for these parts, before the silence.

    It follows `join` exactly: each joint overlaps the two parts by `overlap`
    frames, or by the shorter part when a part is shorter than that.
    """
    total = intro
    for piece in middle + [outro]:
        total += piece - min(overlap, total, piece)
    return total


def plan(target: int, intro: int, edges: list[int], outro: int, overlap: int) -> Plan:
    """Return the most middle bars that fit before the outro, in whole frames.

    `edges` holds the frame position of each bar line in the middle part,
    from 0 to the end of the part.
    """
    bars = len(edges) - 1
    if bars < 1:
        raise ThemeError("The middle part must have one bar or more.")
    if edges[0] != 0:
        raise ThemeError("The first bar line of the middle part must be at frame 0.")
    if min(edges[i + 1] - edges[i] for i in range(bars)) <= overlap:
        raise ThemeError("Each bar of the middle part must be longer than a joint (10 ms).")
    used = length(intro, [], outro, overlap)
    if used > target:
        raise ThemeError(
            "The video is shorter than the intro and the outro together. "
            "For a video this short, use the outro alone."
        )
    count = 0
    while True:
        longer = length(intro, pieces(count + 1, bars, edges), outro, overlap)
        if longer > target:
            return Plan(middle_bars=count, pad=target - used)
        count, used = count + 1, longer


@dataclass
class Part:
    params: wave._wave_params
    samples: array.array

    @property
    def frames(self) -> int:
        return len(self.samples) // self.params.nchannels



def read_part(path: Path) -> Part:
    if not path.exists():
        raise ThemeError(f"Missing part: {path}")
    with wave.open(str(path), "rb") as wav:
        params = wav.getparams()
        if params.sampwidth != 2:
            raise ThemeError(f"{path.name} is not 16-bit PCM. Convert it with ffmpeg first (README.md).")
        samples = array.array("h")
        samples.frombytes(wav.readframes(params.nframes))
    if sys.byteorder == "big":
        samples.byteswap()
    return Part(params=params, samples=samples)


def join(out: array.array, piece: array.array, overlap: int, channels: int) -> None:
    """Append `piece` to `out`, with a linear crossfade over `overlap` frames.

    Every channel of one frame gets the same gain, so the balance holds.
    """
    frames = min(overlap, len(out) // channels, len(piece) // channels)
    start = len(out) - frames * channels
    for frame in range(frames):
        fade = (frame + 1) / (frames + 1)
        for channel in range(channels):
            i = frame * channels + channel
            mixed = round(out[start + i] * (1 - fade) + piece[i] * fade)
            out[start + i] = max(-32768, min(32767, mixed))
    out.extend(piece[frames * channels:])


def fit(target: float, parts_dir: Path, mix: str) -> tuple[wave._wave_params, array.array]:
    theme = json.loads((parts_dir / "theme.json").read_text(encoding="utf-8"))
    bars = theme.get("middle_bars")
    if not isinstance(bars, int) or isinstance(bars, bool) or bars < 1:
        raise ThemeError("theme.json must give middle_bars as a whole number of 1 or more.")
    intro, middle, outro = (read_part(parts_dir / mix / f"{name}.wav") for name in ("intro", "middle", "outro"))
    for part in (middle, outro):
        if (part.params.nchannels, part.params.framerate) != (intro.params.nchannels, intro.params.framerate):
            raise ThemeError("The three parts must have the same rate and channels.")

    channels, rate = intro.params.nchannels, intro.params.framerate
    overlap = round(JOIN_SECONDS * rate)
    edges = [round(i * middle.frames / bars) for i in range(bars + 1)]
    result = plan(round(target * rate), intro.frames, edges, outro.frames, overlap)

    out = array.array("h", intro.samples)
    for piece in pieces(result.middle_bars, bars, edges):
        join(out, middle.samples[:piece * channels], overlap, channels)
    join(out, outro.samples, overlap, channels)
    out.extend([0] * (result.pad * channels))
    return intro.params, out


def write(path: Path, params: wave._wave_params, samples: array.array) -> None:
    data = array.array("h", samples)
    if sys.byteorder == "big":
        data.byteswap()
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(params.nchannels)
        wav.setsampwidth(2)
        wav.setframerate(params.framerate)
        wav.writeframes(data.tobytes())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fit the Ağustos main theme to the length of a video.")
    parser.add_argument("seconds", type=float, help="length of the video in seconds")
    parser.add_argument("out", type=Path, help="the WAV file to write")
    parser.add_argument("--mix", choices=("full", "voice"), default="full",
                        help="full for a video with music only, voice for a video with speech")
    parser.add_argument("--parts", type=Path, default=DEFAULT_PARTS, help="the folder of the theme parts")
    args = parser.parse_args(argv)
    try:
        params, samples = fit(args.seconds, args.parts, args.mix)
    except ThemeError as error:
        print(f"fit_theme.py: {error}", file=sys.stderr)
        return 1
    write(args.out, params, samples)
    print(f"{args.out}: {len(samples) / params.nchannels / params.framerate:.2f} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
