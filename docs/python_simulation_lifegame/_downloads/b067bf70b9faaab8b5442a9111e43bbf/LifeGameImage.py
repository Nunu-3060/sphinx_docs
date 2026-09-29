import numpy as np
from PIL import Image, ImageTk

from LifeGame import LifeGame
from utility import hsv2rgb


class LifeGameImage(LifeGame):
    def __init__(
        self,
        rule: list[list[int]] | None = None,
        width: int = 256,
        height: int = 256,
        probability: float = 0.3,
        tb: bool = True,
        lr: bool = True,
        c0: np.typing.NDArray[np.uint8] | None = None,
        c1: np.typing.NDArray[np.uint8] | None = None,
        pixel: int = 2,
    ) -> None:

        super().__init__(rule, width, height, probability, tb, lr)

        # c0, c1 片方のみの指定は不完全な入力とする。
        if c0 is None or c1 is None:
            rng: np.random.Generator = np.random.default_rng()
            hue: float = float(rng.random())
            saturation: float = 0.875
            value: float = 0.875
            c0 = hsv2rgb(hue, saturation, 1-value)
            c1 = hsv2rgb(hue, saturation, value)
        self.c0: np.typing.NDArray[np.uint8] = c0
        self.c1: np.typing.NDArray[np.uint8] = c1

        self.image_size: tuple[int, int] = (pixel*width, pixel*height)

        self.image_array: np.typing.NDArray[np.uint8] = np.zeros((height, width, 3), dtype=np.uint8)

        return None

    def image_np(self) -> np.typing.NDArray[np.uint8]:
        self.image_array[self.lattice == 0] = self.c0
        self.image_array[self.lattice == 1] = self.c1
        return self.image_array

    def image_pil(self) -> Image.Image:
        im: Image.Image = Image.fromarray(self.image_np())
        return im.resize(self.image_size, resample=Image.Resampling.NEAREST)

    def image_tk(self) -> ImageTk.PhotoImage:
        return ImageTk.PhotoImage(self.image_pil())
