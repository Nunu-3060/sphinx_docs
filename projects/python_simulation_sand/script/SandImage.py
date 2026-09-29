import numpy as np
from PIL import Image, ImageTk

from Sand import Sand


class SandImage(Sand):
    def __init__(
        self,
        width: int = 128,
        height: int = 128,
        L0: float = 2,
        b: float = 4,
        q: float = 0.1,
        D: float = 0.2,
        seed: int | None = None,
        pixel: int = 4,
        hue: float | None = None,
        saturation: float = 0.875,
    ) -> None:
        super().__init__(width, height, L0, b, q, D, seed)
        self.image_size: tuple[int, int] = (pixel*width, pixel*height)
        if hue is None:
            rng: np.random.Generator = np.random.default_rng()
            hue = rng.random()
        self.hue: np.typing.NDArray[np.float64] = np.full((height, width, 3), hue % 1, np.float64)
        self.saturation: np.typing.NDArray[np.float64] = np.full(
            (height, width, 3),
            np.clip(saturation, 0, 1),
            np.float64,
        )
        self.phase_offsets = np.zeros((height, width, 3), np.float64)
        self.phase_offsets[:, :, 1] = 2 / 3
        self.phase_offsets[:, :, 2] = 1 / 3
        return None

    def image_np(self) -> np.typing.NDArray[np.uint8]:
        height_max: np.float64 = self.height.max()
        height_min: np.float64 = self.height.min()
        denom: np.float64 = height_max - height_min
        value: np.typing.NDArray[np.float64] = (
            (self.height - height_min) / (height_max - height_min)
            if 0 < denom else
            np.zeros_like(self.height)
        )
        value = value[:, :, None]
        rgb: np.typing.NDArray[np.float64] = np.clip(
            ((np.clip(
                np.abs(np.mod(self.hue + self.phase_offsets, 1) * 6 - 3) - 1,
                0,
                1,
            ) - 1) * self.saturation + 1) * value,
            0,
            1,
        )
        return (rgb * 255).round(0).astype(np.uint8)

    def image_pil(self) -> Image.Image:
        im: Image.Image = Image.fromarray(self.image_np())
        return im.resize(self.image_size, resample=Image.Resampling.NEAREST)

    def image_tk(self) -> ImageTk.PhotoImage:
        return ImageTk.PhotoImage(self.image_pil())
