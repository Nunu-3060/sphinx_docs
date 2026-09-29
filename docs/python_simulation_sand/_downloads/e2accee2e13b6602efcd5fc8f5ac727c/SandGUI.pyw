import random
import tkinter as tk
from tkinter import ttk

from FrameSand import FrameSand
from SandImage import SandImage
from TkWidget import DISPLAY_SIZE, FrameScale, FrameRadioButton


class SandGUI(ttk.Frame):
    def __init__(self, master: tk.Misc | None = None) -> None:
        super().__init__(master)
        self.top: tk.Toplevel | None = None
        self.frame: dict[str, ttk.Frame] = {
            "color": ttk.Frame(self),
            "size": ttk.Frame(self),
            "button": ttk.Frame(self),
        }
        self.scale: dict[str, FrameScale] = {
            "hue": FrameScale(self.frame["color"], text="hue"),
            "saturation": FrameScale(self.frame["color"], text="saturation"),
        }
        self.size_selector: FrameRadioButton = FrameRadioButton(self.frame["size"])
        self.button: dict[str, ttk.Button] = {
            "start": ttk.Button(self.frame["button"], text="start", state=tk.ACTIVE, command=self.start),
            "stop": ttk.Button(self.frame["button"], text="stop", state=tk.DISABLED, command=self.stop),
            "reset": ttk.Button(self.frame["button"], text="reset", state=tk.ACTIVE, command=self.set_size),
            "color": ttk.Button(self.frame["button"], text="color", state=tk.ACTIVE, command=self.set_color),
        }
        for frame in self.frame.values():
            frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        for scale in self.scale.values():
            scale.pack(side=tk.TOP, fill=tk.BOTH)
        self.size_selector.pack(side=tk.LEFT, fill=tk.BOTH)
        for button in self.button.values():
            button.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.set_size()
        self.set_color()
        return None

    def start(self) -> None:
        self.button["start"].configure(state=tk.DISABLED)
        self.button["stop"].configure(state=tk.ACTIVE)
        wh: int = self.size_selector.get()
        pixel: int = DISPLAY_SIZE // wh
        si: SandImage = SandImage(
            width=wh,
            height=wh,
            pixel=pixel,
            hue=self.scale["hue"].get(),
            saturation=self.scale["saturation"].get(),
        )
        self.top = tk.Toplevel(self)
        self.top.bind("<Destroy>", self._on_destroy)
        self.top.title("Sand")
        fs: FrameSand = FrameSand(self.top, sandimage=si)
        fs.pack()
        return None

    def _on_destroy(self, event: tk.Event) -> None:
        if event.widget is self.top:
            self.button["start"].configure(state=tk.ACTIVE)
            self.button["stop"].configure(state=tk.DISABLED)
        return None

    def stop(self) -> None:
        if self.top is not None and self.top.winfo_exists():
            self.top.destroy()
        return None

    def set_size(self) -> None:
        self.size_selector.set(DISPLAY_SIZE // 2)
        return None

    def set_color(self) -> None:
        self.scale["hue"].set(random.random())
        self.scale["saturation"].set(0.875)
        return None


def main() -> None:
    root: tk.Tk = tk.Tk()
    root.title("Sand")
    SandGUI(root).pack()
    root.mainloop()
    return None


if __name__ == "__main__":
    main()
