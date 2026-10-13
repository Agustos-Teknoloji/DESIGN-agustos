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
- `voice` is for a video with speech. It is quieter and leaves room for the voice.
- The file has the exact length of the video. The intro plays first, the middle part repeats in whole bars, the outro plays last, and silence fills the rest of the last bar.
- The script refuses a video shorter than the intro and the outro together (about 12 s). Put the outro alone under such a video.

## Files

| File | What it is |
|---|---|
| `main-theme/theme.json` | The tempo and the number of bars in the middle part. |
| `main-theme/full/intro.wav`, `middle.wav`, `outro.wav` | The three parts of the full mix. |
| `main-theme/voice/intro.wav`, `middle.wav`, `outro.wav` | The same parts, mixed to sit under speech. |
| `main-theme/master.wav` | The track as it came from the tool, before the cuts. |
| `main-theme/LICENCE.md` | The tool, the plan, the date, the prompt and the proof of the commercial right. |
| `fit_theme.py` | Fits the theme to the length of a video. Python standard library only. |

Every part is 16-bit PCM WAV, 48 kHz, stereo. The `main-theme/` folder does not exist yet. It comes with the theme.

## Make the theme

Suno makes the theme in one song. An agent then cuts the song into the three parts.

### 1. Make the song with Suno

Since 2026-09-03 the Suno terms give the commercial right to a song that you download during a paid plan. The right stays after you cancel. One month of the Pro plan is enough.

Settings: Custom mode, Instrumental on, the newest model, the title `Ağustos main theme`. Under More options, set Weirdness to about 20 percent and Style influence to about 80 percent.

Style field:

```
Calm, warm, smart instrumental brand theme. Soft electronic tones, warm electric piano, felt piano, a soft bell-like lead for a short melody, warm round bass, light soft beat with brushed shaker. 100 BPM, 4/4, D major. Lightly moving, gentle and optimistic, like morning sun in a bright studio. Technology feel, but not a software advert. Even dynamics from start to end. Clean, modern, minimal Scandinavian production with Mediterranean warmth.
```

Exclude styles field:

```
vocals, choir, drop, riser, EDM, dubstep, epic, cinematic, orchestral, trailer, ukulele, whistling, hand claps, glockenspiel, lo-fi crackle, distorted guitar, heavy drums
```

Lyrics field:

```
[Intro]
[Instrumental: soft pad on D major, a bell-like electric piano plays a short rising four-note motif, A D E A, like a sunrise]

[Main Theme]
[Instrumental: soft beat and warm bass enter, chord loop D, A, B minor, G, two bars each, steady and calm]

[Main Theme]
[Instrumental: same chord loop, light piano movement, no new melody]

[Main Theme]
[Instrumental: same chord loop, same energy, no build-up]

[Outro]
[Instrumental: beat stops, the motif returns falling, A E D, like a sunset, ends on a long held D major chord that fades naturally]

[End]
```

1. Press Create. Suno makes two songs.
2. Keep a song that is calm, has no vocals, opens with a short rising melody and ends on a held chord. Suno treats the notes in the brackets as guidance, so the melody can differ. The melody of the chosen song becomes the signature.
3. If no song fits, press Create again with no change.
4. Download the chosen song as WAV while the plan is active. Keep the plan receipt and the download date.
5. Cancel the plan at suno.com/account.

### 2. Cut the parts

An agent cuts the chosen song:

1. Measure the tempo and the first downbeat. Suno can drift from 100 bpm, so measure, never assume.
2. Intro: the bars of the rising melody, before the beat starts (about 5 s).
3. Middle part: 8 bars from a D bar, D, A, B minor and G for two bars each (about 19 s). Play it three times in a row and listen at each joint.
4. Outro: the falling melody, the held chord and its natural decay (about 6 to 8 s).
5. Convert each part to 16-bit PCM WAV, 48 kHz, stereo:

   ```bash
   ffmpeg -i song.wav -ss START -t LENGTH -ar 48000 -ac 2 -c:a pcm_s16le part.wav
   ```

6. Make the voice mix of each part: 12 dB quieter, with a soft dip where speech sits.

   ```bash
   ffmpeg -i full/middle.wav -af "volume=-12dB,equalizer=f=2500:t=q:w=1:g=-4" -c:a pcm_s16le voice/middle.wav
   ```

7. Write `theme.json` with the measured tempo and `"middle_bars": 8`, and `LICENCE.md` with the plan, the date and the Suno fields above.
8. Fit the theme to 30 s and to 67.4 s with `fit_theme.py`, and send both to Emre.
