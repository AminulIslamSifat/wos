import argparse
import subprocess
import tempfile
import time
from pathlib import Path
from datetime import datetime
import cv2
import threading
import numpy as np


def ts():
    return datetime.now().strftime("%Y%m%d_%H%M%S")



latest_frame = None
lock = threading.Lock()
MKV_MAX_SIZE_BYTES = 5 * 1024 * 1024 * 1024


def start_ffmpeg_stream(mkv_path):
    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel", "error",
        "-i", str(mkv_path),
        "-f", "rawvideo",
        "-pix_fmt", "bgr24",
        "pipe:1",
    ]
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=10**8)


def stop_recording(scrcpy_proc, ffmpeg_proc, stop_event, reader_thread):
    stop_event.set()

    if ffmpeg_proc.poll() is None:
        ffmpeg_proc.terminate()
        ffmpeg_proc.wait()

    reader_thread.join(timeout=1.0)

    if scrcpy_proc.poll() is None:
        scrcpy_proc.terminate()
        scrcpy_proc.wait()


def start_recording(mkv, out_dir):
    scrcpy_cmd = [
        "scrcpy",
        "--turn-screen-off",
        "--no-audio",
        "--window-width", "1080",
        "--window-height", "2460",
        "--max_size", "2460",
        "--record", str(mkv),
        "--record-format=mkv",
    ]

    print("[*] Starting scrcpy...")
    scrcpy_proc = subprocess.Popen(scrcpy_cmd)

    # Wait for recording to start and the file to become readable for ffmpeg.
    while not mkv.exists() or mkv.stat().st_size < 8000:
        if scrcpy_proc.poll() is not None:
            raise RuntimeError("scrcpy exited early")
        time.sleep(0.3)

    print("[✓] Recording started\n")

    stop_event = threading.Event()
    ffmpeg_proc = start_ffmpeg_stream(mkv)
    reader_thread = threading.Thread(
        target=reader,
        args=(ffmpeg_proc, out_dir, stop_event),
        daemon=True,
    )
    reader_thread.start()

    return scrcpy_proc, ffmpeg_proc, stop_event, reader_thread


def reader(proc, out_dir, stop_event, width=1080, height=2456):
    
    global latest_frame
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    frame_size = width * height * 3
    frame_index = 0

    while not stop_event.is_set():
        t1 = time.time()
        raw = proc.stdout.read(frame_size)
        t2 = time.time()
        print(f"{t2-t1}s")

        # `read` may return partial buffers before ffmpeg produces a full frame.
        if not raw:
            if proc.poll() is not None:
                break
            time.sleep(0.01)
            continue

        if len(raw) < frame_size:
            if proc.poll() is not None:
                break
            continue

        frame = np.frombuffer(raw, np.uint8)
        try:
            frame = frame.reshape((height, width, 3))
        except ValueError:
            break

        frame_path = out_dir / f"frame_{ts()}_{frame_index:05d}.png"
        cv2.imwrite(str(frame_path), frame)
        frame_index += 1

        with lock:
            latest_frame = frame
        t2 = time.time()
        print(t2-t1)


def capture(interval, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        mkv = Path(tmp) / "screen.mkv"

        try:
            scrcpy_proc, ffmpeg_proc, stop_event, reader_thread = start_recording(mkv, out_dir)
        except RuntimeError as exc:
            print(f"[!] {exc}")
            return

        try:
            while True:
                if ffmpeg_proc.poll() is not None:
                    print("[!] ffmpeg reader exited")
                    break

                if scrcpy_proc.poll() is not None:
                    print("[!] scrcpy exited")
                    break

                if mkv.exists() and mkv.stat().st_size >= MKV_MAX_SIZE_BYTES:
                    size_gb = mkv.stat().st_size / (1024**3)
                    print(f"[!] MKV reached {size_gb:.2f} GB. Restarting recording to clear file...")

                    stop_recording(scrcpy_proc, ffmpeg_proc, stop_event, reader_thread)

                    if mkv.exists():
                        mkv.unlink()

                    try:
                        scrcpy_proc, ffmpeg_proc, stop_event, reader_thread = start_recording(mkv, out_dir)
                    except RuntimeError as exc:
                        print(f"[!] {exc}")
                        break

                time.sleep(max(interval, 0.1))

        except KeyboardInterrupt:
            print("\n[!] stopping...")

        finally:
            stop_recording(scrcpy_proc, ffmpeg_proc, stop_event, reader_thread)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval", type=float, default=2.0)
    parser.add_argument("--output", default="frames")
    args = parser.parse_args()

    capture(args.interval, args.output)