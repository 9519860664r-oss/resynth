# Resynth

Resynth is a Codex skill for analyzing audio, designing editable synthesizer presets and checking their sound against real renders.

## Use

Place this repository in a Codex skills directory as **resynth**. Start a chat and invoke **$resynth** with an audio reference or a sound-design brief. Name the synthesizer when you know which one you want.

> Use $resynth to recreate this bass in Serum 2. Give me the preset, a one-shot WAV and a comparison spectrogram.

The skill tunes pitched patches to C, reports the source tuning and checks the spectral details that give the reference its character. For Serum 2, it can use the last-note audio export to capture the patch.

The optional comparison helper uses Python 3 and FFmpeg. [Usage and interpretation](references/audio-analysis.md)
