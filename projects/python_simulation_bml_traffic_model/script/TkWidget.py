import tkinter as tk
from tkinter import ttk

import numpy as np

from utility import hsv2rgb

#: Display Size
DISPLAY_SIZE: int = 512


class FrameHSV(ttk.Frame):
    def __init__(self, master: tk.Misc | None = None, text: str = "color") -> None:
        super().__init__(master)
        self.frame: dict[str, ttk.Frame] = {
            "top": ttk.Frame(self),
            "h": ttk.Frame(self),
            "s": ttk.Frame(self),
            "v": ttk.Frame(self),
        }
        self.label: dict[str, ttk.Label] = {
            "text": ttk.Label(self.frame["top"], text=text),
            "color": ttk.Label(self.frame["top"]),
            "h": ttk.Label(self.frame["h"], text="hue"),
            "s": ttk.Label(self.frame["s"], text="saturation"),
            "v": ttk.Label(self.frame["v"], text="value"),
        }
        self.scale: dict[str, ttk.Scale] = {
            "h": ttk.Scale(self.frame["h"], from_=0.0, to=1.0, value=0.0, orient=tk.HORIZONTAL, command=self.apply),
            "s": ttk.Scale(self.frame["s"], from_=0.0, to=1.0, value=0.0, orient=tk.HORIZONTAL, command=self.apply),
            "v": ttk.Scale(self.frame["v"], from_=0.0, to=1.0, value=0.0, orient=tk.HORIZONTAL, command=self.apply),
        }
        for k, frame in self.frame.items():
            if k == "top":
                frame.pack(fill=tk.BOTH, expand=True)
            else:
                frame.pack(fill=tk.BOTH)
        for k, label in self.label.items():
            if k == "color":
                label.pack(fill=tk.BOTH, expand=True)
            else:
                label.pack(fill=tk.BOTH)
        for k, v in self.scale.items():
            v.pack(fill=tk.BOTH)
        self.apply()
        return None

    def get(self) -> np.typing.NDArray[np.uint8]:
        return hsv2rgb(self.scale["h"].get(), self.scale["s"].get(), self.scale["v"].get())

    def set(self, h: float, s: float, v: float) -> None:
        self.scale["h"].set(h)
        self.scale["s"].set(s)
        self.scale["v"].set(v)
        return None

    def apply(self, value: str = "") -> None:
        h: float = self.scale["h"].get()
        s: float = self.scale["s"].get()
        v: float = self.scale["v"].get()
        bg: str = "#" + "".join(f"{i:02X}" for i in hsv2rgb(h, s, v))
        fg: str = "#" + "".join(f"{i:02X}" for i in hsv2rgb(1-h, 1-s, 1-v))
        self.label["color"].configure(background=bg, foreground=fg, text=bg, anchor=tk.CENTER)
        return None


class FrameRadioButton(ttk.Frame):
    def __init__(self, master: tk.Misc | None = None) -> None:
        super().__init__(master)
        self.label: ttk.Label = ttk.Label(self, text="size")
        self.value: tk.IntVar = tk.IntVar(self, value=DISPLAY_SIZE // 2)
        self.radiobutton: dict[int, ttk.Radiobutton] = {
            i: ttk.Radiobutton(self, variable=self.value, value=i, text=int(i))
            for i in [DISPLAY_SIZE // 4, DISPLAY_SIZE // 2, DISPLAY_SIZE]
        }
        self.label.pack()
        for v in self.radiobutton.values():
            v.pack()
        return None

    def get(self) -> int:
        return self.value.get()

    def set(self, value: int = DISPLAY_SIZE // 2) -> None:
        if value in self.radiobutton.keys():
            self.value.set(value)
        return None


class FrameScale(ttk.Frame):
    def __init__(self, master: tk.Misc | None = None) -> None:
        super().__init__(master)
        self.label: ttk.Label = ttk.Label(self)
        self.scale: ttk.Scale = ttk.Scale(self, from_=0.0, to=1.0, value=0.0, orient=tk.HORIZONTAL, command=self.apply)
        self.label.pack(side=tk.TOP, fill=tk.BOTH)
        self.scale.pack(side=tk.TOP, fill=tk.BOTH)
        self.apply()
        return None

    def get(self) -> float:
        return self.scale.get()

    def set(self, p: float) -> None:
        self.scale.set(p)
        return None

    def apply(self, value: str = "") -> None:
        p: float = self.scale.get()
        self.label.configure(text=f"probability: {p:.2f}")
        return None
