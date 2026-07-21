import subprocess, platform, shutil
from pathlib import Path
from pystyle import Col
from tqdm import tqdm

black = Col.black
green = Col.green
res = Col.reset
red = Col.red

lightb = Col.StaticMIX((Col.light_blue, Col.blue, Col.light_blue))
purple = Col.StaticMIX((Col.purple, Col.blue, Col.purple))
blued = Col.StaticMIX((Col.black, Col.blue, Col.dark_gray))

class AudioProcessor:
    def __init__(self, ffmpeg_path=None, ffprobe_path=None):
        self.ffmpeg = ffmpeg_path if ffmpeg_path else ("ffmpeg.exe" if platform.system() == "Windows" else "ffmpeg")
        self.ffprobe = ffprobe_path if ffprobe_path else ("ffprobe.exe" if platform.system() == "Windows" else "ffprobe")

        if not shutil.which(self.ffmpeg):
            raise EnvironmentError("ffmpeg not found in PATH")
        if not shutil.which(self.ffprobe):
            raise EnvironmentError("ffprobe not found in PATH")

    def _get_duration(self, input_file):
        cmd = [
            self.ffprobe, "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(input_file)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return float(result.stdout.strip())

    def convert(self, input_file, output_file, sample_rate=None, bit_depth=None, codec=None, use_soxr=True):
        output_path = Path(output_file)
        output_ext = output_path.suffix.lower()

        duration = self._get_duration(input_file)

        cmd = [
            self.ffmpeg, "-y", "-hide_banner",
            "-i", str(input_file),
            "-progress", "pipe:1",
            "-nostats"
        ]

        if sample_rate:
            cmd += ["-ar", str(sample_rate)]

        if use_soxr and output_ext in [".flac", ".wav"]:
            cmd += ["-af", "aresample=resampler=soxr:precision=28"]

        if bit_depth:
            lossy_codecs = ["mp3", "aac", "opus"]
            if codec and codec.lower() in lossy_codecs:
                sample_fmt_map = {16: "s16p", 24: "s32p", 32: "fltp"}
            else:
                sample_fmt_map = {16: "s16", 24: "s32", 32: "s32"}

            sample_fmt = sample_fmt_map.get(bit_depth)
            if not sample_fmt:
                raise ValueError(f"Unsupported bit depth {bit_depth} for codec {codec}")
            cmd += ["-sample_fmt", sample_fmt]

        if codec:
            cmd += ["-c:a", codec]
            if codec.lower() == "mp3":
                cmd += ["-b:a", "320k"]

        cmd.append(str(output_file))
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, bufsize=1)
        pbar = tqdm(total=duration, desc=normal("Processing"), unit="sec", smoothing=0.1, ncols=90, bar_format=f"{res}{{desc}} {lightb}|{{bar}}|{purple} {{percentage:6.2f}}%{res}")

        try:
            for line in process.stdout:
                if line.startswith("out_time_ms"):
                    _, value = line.strip().split("=", 1)

                    try:
                        time_ms = int(value)
                        current = time_ms / 1_000_000
                    except ValueError:
                        continue

                elif line.startswith("out_time"):
                    _, value = line.strip().split("=", 1)

                    if value == "N/A":
                        continue

                    # convert HH:MM:SS.ms → detik
                    try:
                        h, m, s = value.split(":")
                        current = int(h) * 3600 + int(m) * 60 + float(s)
                    except:
                        continue

            process.wait()
            if process.returncode != 0:
                raise RuntimeError("FFmpeg failed")

        finally:
            pbar.close()

def normal(text, symbol = '!'):
    col1 = purple
    col2 = res
    return f" {Col.Symbol(symbol, col2, col1, '[', ']')} {col2}{text}"