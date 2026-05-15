"""Convert head_depth.yuv (Z16/uint16, 1280x800) to RGB colormap PNGs."""

import shutil
from pathlib import Path

import cv2
import numpy as np

SRC = Path(__file__).parent / "head_depth.yuv"
OUT = Path(__file__).parent / "head_depth_rgb"

GLOBAL_HEADER = 256
FRAME_HEADER = 176
WIDTH = 1280
HEIGHT = 800
FRAME_DATA_SIZE = WIDTH * HEIGHT * 2  # uint16

INVALID = {0, 43690}   # 0 = no reading, 0xAAAA = padding sentinel


def read_frame(f, frame_idx: int) -> np.ndarray | None:
    offset = GLOBAL_HEADER + frame_idx * (FRAME_HEADER + FRAME_DATA_SIZE) + FRAME_HEADER
    f.seek(offset)
    raw = f.read(FRAME_DATA_SIZE)
    if len(raw) < FRAME_DATA_SIZE:
        return None
    return np.frombuffer(raw, dtype=np.uint16).reshape(HEIGHT, WIDTH)


def depth_to_rgb(depth: np.ndarray) -> np.ndarray:
    valid = (depth > 0) & (depth != 43690)

    if not valid.any():
        return np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

    # Map valid depths to 0-255 using 1st-99th percentile clipping
    lo = float(np.percentile(depth[valid], 1))
    hi = float(np.percentile(depth[valid], 99))
    gray8 = np.zeros(depth.shape, dtype=np.uint8)
    if hi > lo:
        gray8[valid] = np.clip(
            (depth[valid].astype(np.float32) - lo) / (hi - lo) * 255, 0, 255
        ).astype(np.uint8)

    # Histogram equalization on valid pixels only so near/far spread across
    # the full colormap range instead of clustering at one end.
    vals = gray8[valid]
    hist, _ = np.histogram(vals, bins=256, range=(0, 256))
    cdf = hist.cumsum().astype(np.float64)
    cdf_min = float(cdf[cdf > 0].min())
    n = int(valid.sum())
    lut = np.clip(
        np.round((cdf - cdf_min) / max(n - cdf_min, 1) * 255), 0, 255
    ).astype(np.uint8)

    gray8_eq = np.zeros_like(gray8)
    gray8_eq[valid] = lut[gray8[valid]]

    rgb = cv2.applyColorMap(gray8_eq, cv2.COLORMAP_JET)
    rgb[~valid] = 0   # invalid pixels → black
    return rgb


def main():
    file_size = SRC.stat().st_size
    n_frames = (file_size - GLOBAL_HEADER) // (FRAME_HEADER + FRAME_DATA_SIZE)
    print(f"File: {SRC.name}  |  Frames: {n_frames}  |  Resolution: {WIDTH}x{HEIGHT}")

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()

    saved = 0
    with open(SRC, "rb") as f:
        for i in range(n_frames):
            depth = read_frame(f, i)
            if depth is None:
                print(f"\n  Frame {i:04d}: truncated, skipping")
                continue
            rgb = depth_to_rgb(depth)
            cv2.imwrite(str(OUT / f"frame_{i:04d}.png"), rgb)
            saved += 1
            if saved % 50 == 0 or i == n_frames - 1:
                print(f"  {saved}/{n_frames} frames processed...", end="\r", flush=True)

    print(f"\nDone. {saved} images saved to {OUT}/")


if __name__ == "__main__":
    main()
