# Audio analysis and comparison

## Reproducible measurements

Use [audio_check.py](../scripts/audio_check.py) for a stereo-aware band report and an optional common-scale spectrogram. It requires Python 3 and FFmpeg with the showspectrumpic filter. Choose a window after the transient to analyze the body. Inspect the attack separately. Use a common duration inside both files for comparisons.

    python scripts/audio_check.py reference.wav
    python scripts/audio_check.py reference.wav native.wav --start 0.10 --duration 1.25 --png comparison.png

The report includes peaks, RMS, mid/side level, band power and strong local spectral peaks. The inputs retain their pitch and level, so align or transpose diagnostic copies separately where needed. Use a longer FFT or direct periodicity analysis to resolve nearby low frequencies.

## Read the spectrum

- Estimate the fundamental from steady timing and the spacing of several narrow peaks. Interpolated FFT peaks from long windows can distinguish small cents offsets. Validate the spacing against independent bands. A waveform can have several zero crossings per cycle or a weak fundamental.
- Track features across windows. Harmonic comb spacing, persistence and correlated envelopes can show that a bright band belongs to the note. They leave open whether it originated in an oscillator, saturation, alias-producing processing or another layer.
- Compare bands relative to the fundamental or another stable region as well as in dBFS. Use identical color scales, frequency limits and time units. Record absolute pitch and loudness separately from a pitch- and gain-matched view. A linear-frequency zoom makes harmonic line spacing visible.
- Inspect the side channel for wide bass and accents. A quiet side can hold a distinctive upper texture. Preserve relative phase when reconstructing left and right separately, and check the mono sum.

## Design decisions

- Stable harmonics can use additive or wavetable synthesis. Select bandwidth and frame density from measured content and modulation speed. Use anti-aliased resampling and an analysis sample rate that covers the highest retained harmonic.
- Expose a measured high harmonic layer or independent tone on a second oscillator when useful. For decorrelated broadband energy, try shaped noise and match its envelope. EQ acts on existing energy. Use nonlinear processing to generate new harmonics when it fits the evidence.
- Envelope motion affects the spectrum after the attack. Compare onset, sustain and release separately. Measure the audible end before any silence padding. Export duration depends both on the gate and on the patch.
