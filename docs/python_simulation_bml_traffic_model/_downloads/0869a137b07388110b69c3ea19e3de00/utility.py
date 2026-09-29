import numpy as np


def hsv2rgb(
    h: np.typing.NDArray[np.float64] | float,
    s: np.typing.NDArray[np.float64] | float,
    v: np.typing.NDArray[np.float64] | float,
) -> np.typing.NDArray[np.uint8]:
    phase_offsets: np.typing.NDArray[np.float64]
    rgb: np.typing.NDArray[np.float64]
    if isinstance(h, float) and isinstance(s, float) and isinstance(v, float):
        phase_offsets = np.array([0, 2/3, 1/3], np.float64)
        rgb = ((np.clip(np.abs(np.mod(h + phase_offsets, 1) * 6 - 3) - 1, 0, 1) - 1) * s + 1) * v
    elif isinstance(h, np.ndarray) and isinstance(s, np.ndarray) and isinstance(v, np.ndarray):
        if h.shape != s.shape or h.shape != v.shape:
            raise TypeError("adjust the array lengths to be the same.")
        elif len(h.shape) != 2:
            raise TypeError("input 2D numpy array.")
        phase_offsets = np.zeros((h.shape[0], h.shape[1], 3), np.float64)
        phase_offsets[:, :, 1] = 2 / 3
        phase_offsets[:, :, 2] = 1 / 3
        hue: np.typing.NDArray[np.float64] = h[:, :, None]
        saturate: np.typing.NDArray[np.float64] = s[:, :, None]
        value: np.typing.NDArray[np.float64] = v[:, :, None]
        rgb = ((np.clip(np.abs(np.mod(hue + phase_offsets, 1) * 6 - 3) - 1, 0, 1) - 1) * saturate + 1) * value
    else:
        text: str = "\n".join([
            "h, s, and v must all be float or np.ndarray.",
            f"h: {type(h).__name__}",
            f"s: {type(s).__name__}",
            f"v: {type(v).__name__}",
        ])
        raise TypeError(text)
    rgb = np.clip(rgb, 0, 1)
    return (rgb * 255).round(0).astype(np.uint8)
