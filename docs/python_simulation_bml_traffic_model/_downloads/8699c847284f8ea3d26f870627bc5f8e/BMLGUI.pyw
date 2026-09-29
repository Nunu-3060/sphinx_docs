import random
import tkinter as tk
from tkinter import ttk

from BMLImage import BMLImage
from FrameBML import FrameBML
from TkWidget import DISPLAY_SIZE, FrameHSV, FrameRadioButton, FrameScale


class BMLGUI(ttk.Frame):
    def __init__(self, master: tk.Misc | None = None) -> None:
        super().__init__(master)
        self.top: tk.Toplevel | None = None
        # parts
        self.frame: dict[str, ttk.Frame] = {
            "color": ttk.Frame(self),
            "size": ttk.Frame(self),
            "button": ttk.Frame(self),
        }
        self.color: dict[str, FrameHSV] = {
            "zero": FrameHSV(self.frame["color"], text="None"),
            "one": FrameHSV(self.frame["color"], text="car one"),
            "two": FrameHSV(self.frame["color"], text="car two"),
        }
        self.size_selector: FrameRadioButton = FrameRadioButton(self.frame["size"])
        self.probability: FrameScale = FrameScale(self.frame["size"])
        self.button: dict[str, ttk.Button] = {
            "start": ttk.Button(self.frame["button"], text="start", state=tk.ACTIVE, command=self.start),
            "stop": ttk.Button(self.frame["button"], text="stop", state=tk.DISABLED, command=self.stop),
            "reset": ttk.Button(self.frame["button"], text="reset", state=tk.ACTIVE, command=self.set_rule),
            "color": ttk.Button(self.frame["button"], text="color", state=tk.ACTIVE, command=self.set_color),
        }
        # pack
        for frame in self.frame.values():
            frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        for color in self.color.values():
            color.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.size_selector.pack(side=tk.TOP, fill=tk.BOTH)
        self.probability.pack(side=tk.TOP, fill=tk.BOTH)
        for button in self.button.values():
            button.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # set
        self.set_rule()
        self.set_color()
        return None

    def set_rule(self) -> None:
        self.probability.set(0.6)
        self.size_selector.set(DISPLAY_SIZE // 2)
        return None

    def set_color(self) -> None:
        hue: float = random.random()
        saturation: float = 0.875
        value: float = 0.875
        self.color["zero"].set(hue, saturation, 1-value)
        self.color["one"].set((hue-0.125)%1, saturation, value)
        self.color["two"].set((hue+0.125)%1, saturation, value)
        return None

    def start(self) -> None:
        self.button["start"].configure(state=tk.DISABLED)
        self.button["stop"].configure(state=tk.ACTIVE)
        # config
        wh: int = self.size_selector.get()
        pixel: int = DISPLAY_SIZE // wh
        bmli: BMLImage = BMLImage(
            width=wh,
            height=wh,
            probability=self.probability.get(),
            c0=self.color["zero"].get(),
            c1=self.color["one"].get(),
            c2=self.color["two"].get(),
            pixel=pixel,
        )
        # start
        self.top = tk.Toplevel(self)
        self.top.title("Biham-Middleton-Levine Traffic Model")
        self.top.bind("<Destroy>", self._on_destroy)
        fbml: FrameBML = FrameBML(self.top, bmli=bmli)
        fbml.pack()
        return None

    def stop(self) -> None:
        if self.top is not None and self.top.winfo_exists():
            self.top.destroy()
        return None

    def _on_destroy(self, event: tk.Event) -> None:
        if event.widget is self.top:
            self.button["start"].configure(state=tk.ACTIVE)
            self.button["stop"].configure(state=tk.DISABLED)
        return None


def main() -> None:
    root: tk.Tk = tk.Tk()
    root.title("Biham-Middleton-Levine Traffic Model")
    BMLGUI(root).pack()
    root.mainloop()
    return None


if __name__ == "__main__":
    main()
