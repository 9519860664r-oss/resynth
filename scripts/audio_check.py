"""Report audio levels and spectral features on a shared time and frequency scale."""

import argparse
import array
import cmath
import json
import math
import statistics
import subprocess
import sys
import tempfile
from pathlib import Path

RATE = 48000
BANDS = (20, 100, 250, 500, 1000, 2500, 4000, 6000, 8000, 10000, 14500, 20000)


def run(*args, data=None):
    return subprocess.run(args, input=data, capture_output=True, check=True).stdout


def decode(path, start, duration):
    streams = json.loads(run("ffprobe", "-v", "error", "-select_streams", "a:0",
                             "-show_entries", "stream=channels,sample_rate,duration", "-of", "json", str(path)))
    info = streams["streams"][0]
    count = int(info["channels"])
    routing = "stereo|c0=c0|c1=c0" if count == 1 else "stereo|c0=c0|c1=c1"
    limit = ["-t", str(duration)] if duration is not None else []
    raw = run("ffmpeg", "-v", "error", "-ss", str(start), "-i", str(path), *limit,
              "-map", "0:a:0", "-af", "pan=" + routing, "-ar", str(RATE), "-f", "f32le", "pipe:1")
    samples = array.array("f", raw)
    if sys.byteorder != "little":
        samples.byteswap()
    if not samples:
        raise ValueError(f"No audio in the selected window of {path.name}")
    mid = [(a+b)*.5 for a,b in zip(samples[::2],samples[1::2])]
    side = [(a-b)*.5 for a,b in zip(samples[::2],samples[1::2])]
    return info, mid, side


def fft_power(samples):
    size = len(samples)
    bits = size.bit_length()-1
    values = [complex(samples[int(f"{i:0{bits}b}"[::-1],2)]) for i in range(size)]
    step = 2
    while step <= size:
        half = step//2
        roots = [cmath.exp(-2j*math.pi*k/step) for k in range(half)]
        for start in range(0,size,step):
            for k,root in enumerate(roots):
                a,b = start+k,start+k+half
                v = values[b]*root
                values[a],values[b] = values[a]+v,values[a]-v
        step *= 2
    power = [2*abs(v)**2 for v in values[:size//2+1]]
    power[0] *= .5
    power[-1] *= .5
    return power


def power_spectrum(samples, size):
    actual = min(len(samples),size)
    weights = [.5-.5*math.cos(math.tau*(i+.5)/actual) for i in range(actual)]
    positions = sorted({(len(samples)-actual)*k//4 for k in range(5)})
    norm = size*sum(w*w for w in weights)
    spectra = []
    for start in positions:
        windowed = [a*b for a,b in zip(samples[start:start+actual],weights)]
        spectra.append(fft_power(windowed+[0]*(size-actual)))
    return [statistics.fmean(v)/norm for v in zip(*spectra)]


def decibels(power):
    return round(10*math.log10(max(power,1e-24)),2)


def report(info, mid, side, size):
    step = RATE/size
    power = power_spectrum(mid,size)
    bands = {}
    for low,high in zip(BANDS,BANDS[1:]):
        if low >= int(info["sample_rate"])/2:
            continue
        i,j = math.ceil(low/step),math.ceil(high/step)
        points = [k for k in range(max(1,i),min(j,len(power)-1))
                  if power[k]>power[k-1] and power[k]>power[k+1]]
        peaks = sorted(points,key=power.__getitem__,reverse=True)[:4]
        bands[f"{low}-{high} Hz"] = {
            "rms_dbfs":decibels(sum(power[i:j])),
            "peaks_hz_and_bin_dbfs":[[round(k*step,1),decibels(power[k])] for k in peaks],
        }
    rms = decibels(statistics.fmean(v*v for v in mid))
    return {
        "source":info, "used_seconds":round(len(mid)/RATE,5),
        "mid_peak_dbfs":decibels(max(map(abs,mid))**2), "mid_rms_dbfs":rms,
        "side_minus_mid_db":round(decibels(statistics.fmean(v*v for v in side))-rms,2),
        "fft_bin_hz":step, "bands":bands,
    }


def plot(tracks, path, low, high):
    with tempfile.TemporaryDirectory() as temporary:
        images = []
        for i,track in enumerate(tracks):
            target = str(Path(temporary)/f"{i}.png")
            raw = array.array("f",track)
            if sys.byteorder != "little":
                raw.byteswap()
            run("ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(RATE), "-ac", "1", "-i", "pipe:0",
                "-lavfi", f"showspectrumpic=s=700x384:start={low}:stop={high}:color=plasma:drange=110",
                "-frames:v","1","-update","1",target,data=raw.tobytes())
            images.append(target)
        if len(images) == 1:
            path.write_bytes(Path(images[0]).read_bytes())
        else:
            run("ffmpeg", "-v","error","-y","-i",images[0],"-i",images[1],"-lavfi","hstack",
                "-frames:v","1","-update","1",str(path))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reference",type=Path)
    parser.add_argument("render",type=Path,nargs="?")
    parser.add_argument("--start",type=float,default=0)
    parser.add_argument("--duration",type=float)
    parser.add_argument("--fft",type=int,choices=(512,1024,2048,4096,8192,16384,32768,65536),default=32768)
    parser.add_argument("--png",type=Path)
    parser.add_argument("--low",type=int,default=0)
    parser.add_argument("--high",type=int,default=20000)
    args = parser.parse_args()
    if args.start < 0 or (args.duration is not None and args.duration <= 0):
        parser.error("start must be nonnegative and duration must be positive")
    if not 0 <= args.low < args.high <= RATE//2:
        parser.error("plot frequencies must satisfy 0 <= low < high <= 24000")

    files = [args.reference]+([args.render] if args.render else [])
    decoded = [decode(path,args.start,args.duration) for path in files]
    length = min(len(mid) for _,mid,_ in decoded)
    results = [
        {"file":path.name, **report(info,mid[:length],side[:length],args.fft)}
        for path,(info,mid,side) in zip(files,decoded)
    ]
    if args.png:
        plot([mid[:length] for _,mid,_ in decoded],args.png,args.low,args.high)
    print(json.dumps(results,ensure_ascii=True,indent=2))


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        sys.exit(exc.stderr.decode(errors="replace").strip() or str(exc))
