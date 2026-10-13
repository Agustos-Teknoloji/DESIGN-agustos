"""Tests for brand/audio/fit_theme.py, the fit of the main theme to a video."""

import array
import importlib.util
import json
import random
import sys
import tempfile
import unittest
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("fit_theme", ROOT / "brand" / "audio" / "fit_theme.py")
fit_theme = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = fit_theme
SPEC.loader.exec_module(fit_theme)

INTRO, MIDDLE, OUTRO, LAST = 1000, 2000, 3000, 3333


def write_part(path: Path, frames: int, value: int, rate: int, channels: int, last: int | None = None) -> None:
    samples = array.array("h", [value] * frames * channels)
    if last is not None:
        samples[-channels:] = array.array("h", [last] * channels)
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(channels)
        wav.setsampwidth(2)
        wav.setframerate(rate)
        wav.writeframes(samples.tobytes())


def make_parts(folder: Path, rate: int, channels: int, intro: int, middle: int, outro: int, bars: int) -> None:
    (folder / "full").mkdir(parents=True, exist_ok=True)
    (folder / "theme.json").write_text(json.dumps({"bpm": 100, "middle_bars": bars}), encoding="utf-8")
    write_part(folder / "full" / "intro.wav", intro, INTRO, rate, channels)
    write_part(folder / "full" / "middle.wav", middle, MIDDLE, rate, channels)
    write_part(folder / "full" / "outro.wav", outro, OUTRO, rate, channels, last=LAST)


class PlanTest(unittest.TestCase):
    RATE = 48000
    EDGES = [round(i * 19.2 * 48000 / 8) for i in range(9)]  # 100 bpm, 4/4: 8 bars of 2.4 s.
    OVERLAP = 480

    def plan(self, seconds):
        return fit_theme.plan(round(seconds * self.RATE), 230400, self.EDGES, 345600, self.OVERLAP)

    def test_whole_bars_fill_the_room_and_silence_fills_the_rest(self):
        # 67.4 s less 4.8 s and 7.2 s leaves 55.4 s: 23 bars (55.2 s) and 0.2 s.
        result = self.plan(67.4)
        self.assertEqual(result.middle_bars, 23)
        joints = 4  # Two whole middle parts, one piece of 7 bars, then the outro.
        self.assertEqual(result.pad, round(0.2 * self.RATE) + joints * self.OVERLAP)

    def test_one_bar_that_fits_is_played(self):
        # Intro, one bar and outro with two joints need 14.38 s.
        self.assertEqual(self.plan(14.38).middle_bars, 1)
        self.assertEqual(self.plan(14.37).middle_bars, 0)

    def test_a_video_as_long_as_intro_and_outro_has_no_middle(self):
        self.assertEqual(self.plan(11.99).middle_bars, 0)

    def test_bar_lines_that_do_not_start_at_zero_are_refused(self):
        with self.assertRaisesRegex(fit_theme.ThemeError, "frame 0"):
            fit_theme.plan(10, 1, [-2, -1], 1, 0)

    def test_a_video_shorter_than_intro_and_outro_is_refused(self):
        with self.assertRaisesRegex(fit_theme.ThemeError, "outro alone"):
            self.plan(10.0)


class FitTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.parts = Path(self.tmp.name) / "parts"

    def tearDown(self):
        self.tmp.cleanup()

    def check(self, seconds, rate, channels, intro, middle, outro, bars):
        make_parts(self.parts, rate, channels, intro, middle, outro, bars)
        params, samples = fit_theme.fit(seconds, self.parts, "full")
        frames = [samples[i] for i in range(0, len(samples), channels)]
        target = round(seconds * rate)
        overlap = round(fit_theme.JOIN_SECONDS * rate)
        context = dict(seconds=seconds, rate=rate, channels=channels, intro=intro, middle=middle, outro=outro, bars=bars)

        self.assertEqual(len(samples), target * channels, context)
        self.assertIn(LAST, frames, context)  # The last frame of the outro is never cut.
        self.assertGreaterEqual(sum(1 for v in frames if v in (OUTRO, LAST)), outro - overlap - 1, context)
        last = frames.index(LAST)
        self.assertTrue(all(v == 0 for v in frames[last + 1:]), context)  # Only silence after the outro.
        self.assertEqual(frames[0], INTRO, context)
        for frame in range(0, len(samples), channels):  # Each frame has one gain on all channels.
            self.assertEqual(len(set(samples[frame:frame + channels])), 1, context)

        # No extra bar would have fitted.
        edges = [round(i * middle / bars) for i in range(bars + 1)]
        result = fit_theme.plan(target, intro, edges, outro, overlap)
        more = fit_theme.length(intro, fit_theme.pieces(result.middle_bars + 1, bars, edges), outro, overlap)
        self.assertGreater(more, target, context)

    def test_the_documented_lengths(self):
        for seconds in (12.0, 30.0, 65.35, 67.4167, 180.0):
            with self.subTest(seconds=seconds):
                self.check(seconds, 8000, 2, 38400, 153600, 57600, 8)

    def test_the_cases_that_once_cut_the_outro(self):
        self.check(40.77009375, 48000, 2, 230400, 921603, 345600, 8)
        self.check(16.78, 22050, 2, round(4.8 * 22050), round(19.2 * 22050), round(7.2 * 22050), 8)
        self.check(10.8000625, 48000, 1, 230400, 921600, 288003, 8)

    def test_random_parts_rates_and_channels(self):
        rng = random.Random(20261013)
        for _ in range(40):
            rate = rng.choice((8000, 11025, 22050))
            bars = rng.randint(1, 9)
            intro, outro = rng.randint(200, rate * 3), rng.randint(200, rate * 3)
            middle = rng.randint(bars * (rate // 50), rate * 6)
            seconds = (intro + outro) / rate + rng.uniform(0, 10)
            with self.subTest(rate=rate, bars=bars, seconds=seconds):
                self.check(seconds, rate, rng.choice((1, 2, 3)), intro, middle, outro, bars)

    def test_the_command_writes_a_wav_of_the_video_length(self):
        make_parts(self.parts, 8000, 2, 38400, 153600, 57600, 8)
        out = Path(self.tmp.name) / "music.wav"
        self.assertEqual(fit_theme.main(["67.4", str(out), "--parts", str(self.parts)]), 0)
        with wave.open(str(out), "rb") as wav:
            self.assertEqual((wav.getnchannels(), wav.getframerate(), wav.getsampwidth()), (2, 8000, 2))
            self.assertEqual(wav.getnframes(), round(67.4 * 8000))

    def test_a_theme_file_without_bars_is_refused(self):
        make_parts(self.parts, 8000, 2, 38400, 153600, 57600, 8)
        for bars in (0, -1, "8", None):
            with self.subTest(bars=bars):
                (self.parts / "theme.json").write_text(json.dumps({"bpm": 100, "middle_bars": bars}), encoding="utf-8")
                with self.assertRaisesRegex(fit_theme.ThemeError, "middle_bars"):
                    fit_theme.fit(30.0, self.parts, "full")

    def test_a_missing_part_names_the_file(self):
        make_parts(self.parts, 8000, 2, 38400, 153600, 57600, 8)
        (self.parts / "full" / "outro.wav").unlink()
        with self.assertRaisesRegex(fit_theme.ThemeError, "outro.wav"):
            fit_theme.fit(30.0, self.parts, "full")


if __name__ == "__main__":
    unittest.main()
