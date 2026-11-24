---
name: resynth
description: Analyze audio references, reconstruct or design sounds in a user-selected synthesizer, and verify editable presets against native renders. Use for recreating samples, synthesizing from a description, comparing exported patches, and diagnosing tone, transients, harmonics, noise, pitch, or stereo differences that affect resynthesis.
---

# Resynth

Choose the target synth from the request or the established session. Ask when the target is unclear and the requested preset depends on it. For analysis-only requests, work from the audio and report the evidence. For a brief without a reference, translate the desired traits into a patch and verify its render against the brief.

## Analyze the reference

- Inspect the whole file and isolate the target. Measure the attack, body, motion and audible tail. Check channel content, level and spectra across the usable frequency range. If the target is masked, use a timestamp or isolated clip when the missing information affects the result.
- Find a stable fundamental using periodicity and a high-resolution harmonic grid. Cross-check when distortion, a dominant octave, modulation or noise confuses either measurement. Report the measured note and cents. Distinguish a stable note from a pitch sweep or multiple notes.
- Inspect high bands during both the attack and sustain. Repeating line spacing tied to the fundamental supports a harmonic or phase-related component. A broad floor, independent peak or stereo residual suggests a different source. Separate observations from hypotheses about the original instrument, effects and layer count.
- Identify what makes the sound recognizable. Check pitch and amplitude contours, harmonic balance and phase, transient, noise, stereo, beating, modulation and release where relevant. Look for strong narrow bands that disappear in wideband averages. Use [audio analysis](references/audio-analysis.md) for measurement and comparison.

## Design and tune the preset

- Use the simplest editable patch that reproduces the identifying features. Add distinct layers when they account for audible differences. Expose useful controls where feasible. Custom wavetables reconstructed from harmonics are allowed. Ask before embedding audio from the reference as sample playback.
- Tune single-note pitched sounds to concert C in a suitable octave with chromatic key tracking. Confirm sounding octave, MIDI note and frequency because note labels vary between DAWs. Tell the user when the source has a different note or cents offset. For a pitch envelope, tune the stable portion to C and preserve the sweep. For chords with an identifiable root, transpose the root to C and preserve intervals. Report unpitched or uncertain results when a tuning claim lacks evidence.
- Match the whole audible span. Check for accidental high-harmonic truncation, resampling aliases, stereo collapse or premature release. Test neighboring notes where they matter. In a batch, analyze and verify each sound separately and reuse patch architecture where it applies.
- Deliver a native editable preset for the chosen synth. Use an instance the user opened for this task or authorized. Ask before opening the synth, or ask the user to open it. When a native file cannot be produced, report the specific blocker. Give text settings only on request.

## Verify and deliver

- Load the final saved preset and render it in the target synth. Use the same sounding pitch, comparable note length and velocity, and matched listening level for A/B. Record the original tuning, render settings and absolute levels separately. Use float audio to measure over-range peaks before any conversion to fixed-point WAV. For Serum 2, prefer its [last-note one-shot export](references/serum-2.md) when available.
- Compare identifying features and measurements, then iterate on material differences supported by evidence. When the user asks to get even closer, provide matched A/B audio and use their listening feedback to guide the next iteration. The user makes the final subjective call in that mode.
- Give a preset, native WAV render, spectrogram and short comparison per sound. A structural check, model preview or different synth render is separate from native verification. Name any missing artifact, material residual difference or blocker before labeling the work complete.
- Deliver files in chat by default. For a user-specified folder, sort by sound type and reuse suitable existing subfolders. Use separate revision names or obtain permission to replace a preset. Verify the files at the destination. Check a synth's library index separately when the user expects files to appear there.
