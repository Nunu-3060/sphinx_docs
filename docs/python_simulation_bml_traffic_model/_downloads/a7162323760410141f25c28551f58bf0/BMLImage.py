import numpy as np
from PIL import Image, ImageTk

from BML import BML
from utility import hsv2rgb


class BMLImage(BML):
    def __init__(
        self,
        width: int = 256,
        height: int = 256,
        probability: float = 0.6,
        seed: int | None = None,
        c0: np.typing.NDArray[np.uint8] | None = None,
        c1: np.typing.NDArray[np.uint8] | None = None,
        c2: np.typing.NDArray[np.uint8] | None = None,
        pixel: int = 2,
    ) -> None:
        super().__init__(width, height, probability, seed)
        if c0 is None or c1 is None or c2 is None:
            rng: np.random.Generator = np.random.default_rng()
            h: float = rng.random()
            s: float = 0.875
            v: float = 0.875
            c0 = hsv2rgb(h, s, 1-v)
            c1 = hsv2rgb(h-0.125, s, v)
            c2 = hsv2rgb(h+0.125, s, v)
        self.c0: np.typing.NDArray[np.uint8] = c0
        self.c1: np.typing.NDArray[np.uint8] = c1
        self.c2: np.typing.NDArray[np.uint8] = c2
        self.image_array: np.typing.NDArray[np.uint8] = np.zeros((height, width, 3), dtype=np.uint8)
        self.image_size: tuple[int, int] = (pixel*width, pixel*height)
        return None

    def image_np(self) -> np.typing.NDArray[np.uint8]:
        self.image_array[self.lattice == 0] = self.c0
        self.image_array[self.lattice == 1] = self.c1
        self.image_array[self.lattice == 2] = self.c2
        return self.image_array

    def image_pil(self) -> Image.Image:
        im: Image.Image = Image.fromarray(self.image_np())
        return im.resize(self.image_size, resample=Image.Resampling.NEAREST)

    def image_tk(self) -> ImageTk.PhotoImage:
        return ImageTk.PhotoImage(self.image_pil())
