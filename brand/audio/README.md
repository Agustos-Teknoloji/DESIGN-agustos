# The Ağustos main theme

One piece of music for every Ağustos video, of every brand, with or without speech. DESIGN.md ("Sound") holds the rules. This file tells how to make the theme and how to use it.

## Use it in a video

Write this line in the video brief:

> Use the Ağustos main theme. Repeat the middle part as long as the video needs, and end with the outro.

Then make the music file for the length of the video:

```bash
python3 brand/audio/fit_theme.py 67.4 music.wav
python3 brand/audio/fit_theme.py 95 music.wav --mix voice
```

- `full` (the default) is for a video with music and text only.
- `voice` is for a video with speech. It is 12 dB quieter.
- The file has the exact length of the video. The intro plays first, the middle part repeats, the outro plays last, and silence fills the last moment.
- The script refuses a video shorter than 6.2 s, the intro and the outro together. Put the outro alone under such a video.

## Files

| File | What it is |
|---|---|
| `main-theme/theme.json` | The tempo, the number of steps in the middle part (`middle_bars`), the length of each joint (`joint_seconds`) and where the parts come from. |
| `main-theme/full/intro.wav`, `middle.wav`, `outro.wav` | The three parts of the full mix. |
| `main-theme/voice/intro.wav`, `middle.wav`, `outro.wav` | The same parts, mixed to sit under speech. |
| `main-theme/source.wav` | The loop as it came from Suno, before the cuts. |
| `main-theme/LICENCE.md` | The tool, the plan, the date, the brief and the proof of the commercial right. |
| `fit_theme.py` | Fits the theme to the length of a video. Python standard library only. |

Every part is 16-bit PCM WAV, 48 kHz, stereo.

## Make the theme again

The theme exists. Make it again only if Ağustos decides to change it. The steps of 2026-10-13:

### 1. Make the loop with Suno

Use a paid plan: since 2026-09-03 the Suno terms give the commercial right to a sound that a paid subscriber downloads. Open the Sounds tab, set the type to Loop, BPM to 100 and the key to D major. The description field takes 500 characters at most:

```
Ambient background loop, warm and grounded. Cellos and double basses hold long, quiet chords: D, A, Bm, G, two bars each. No melody, no rhythm, no beat. Notes swell gently and fade, like slow breathing. Warm, not dark. Calm, made to sit under speech. No violins, no piano, no drums, no synths, no vocals, no build-up.
```

Keep the loop that you forget is playing when you talk over it. Download it as WAV.

### 2. Cut the parts

1. Measure the level of each second. The loop of 2026-10-13 swells in for about 3 s and fades out for about 2 s.
2. Intro: from the start to the end of the swell (0 to 4.0 s).
3. Middle part: the steady part (4.0 to 15.5 s).
4. Outro: from there to the end, with the fade (15.5 to 19.2 s).
5. Set the level of the middle part to -16 LUFS, and give the intro and the outro the same gain.
6. Make the voice mix of each part, 12 dB quieter:

   ```bash
   ffmpeg -i full/middle.wav -af "volume=-12dB" -c:a pcm_s16le voice/middle.wav
   ```

7. Write `theme.json`: `"middle_bars": 6` gives six cut points in the middle part, and `"joint_seconds": 1.5` gives soft joints. Ambient music needs long joints; music with a beat needs the 10 ms default.
8. Fit the theme to 30 s and to 180 s, and listen at each joint.

## Make the launch version again

The launch version exists in `brand/audio/launch-theme/`. Fit it with `python3 brand/audio/fit_theme.py SECONDS music.wav --parts brand/audio/launch-theme`. Make it again only if Ağustos decides to change it. The steps of 2026-10-13:

1. Use a paid Suno plan. Open the Songs tab: Custom mode, Instrumental on, the title `Ağustos launch theme`.
2. Style field:

   ```
   Instrumental launch version of the Ağustos ambient brand theme. Strings only: cellos, double basses and violas. Warm, grounded and calm, with a gentle forward motion. 100 BPM, 4/4, D major. Cellos and double basses hold long, warm chords, as in the brand theme. Violas and cellos add a soft, steady bowed pulse in quiet eighth notes, so the music moves without drums. Four-chord loop D, A, Bm, G, two bars each, with smooth changes. No melody. The same calm energy from start to end, with one small lift halfway: the violas enter. Natural, intimate recording that sits under on-screen text.
   ```

3. Exclude styles field:

   ```
   piano, electric piano, percussion, drums, kick, shaker, synth, pad, vocals, choir, violin solo, lead melody, pizzicato, drop, riser, build-up, cinematic, epic, full orchestra, brass
   ```

4. Lyrics field, for the order of the layers:

   ```
   [Intro]
   [Instrumental: cellos and double basses alone, long soft chords]

   [Verse]
   [Instrumental: a soft bowed pulse enters in the cellos]

   [Verse]
   [Instrumental: violas enter, same calm energy]

   [Verse]
   [Instrumental: same loop, steady]

   [Outro]
   [Instrumental: the pulse stops, strings hold a long D major chord and fade]

   [End]
   ```

5. Keep the song that sounds like the theme, only gently walking forward. Download it as WAV.
6. Find the tempo and the first downbeat. The song of 2026-10-13 is 99.96 bpm, with the first downbeat at 0.13 s.
7. Find how many bars the harmony takes to repeat. Compare each bar with the bar 8 and 16 bars later; the song of 2026-10-13 repeats every 16 bars.
8. Choose the middle part as one full repeat, where the bar after it sounds most like its first bar. The song of 2026-10-13 uses bars 4 to 19, with the first downbeat as bar 1.
9. Cut the intro, the middle part and the outro, as for the theme. Set the middle part to -16 LUFS, and make the voice mix 12 dB quieter.
10. Write `theme.json` with `"middle_bars"` set to the repeat length and `"joint_seconds": 0.05`. A part with a pulse needs a short joint at a bar line.
