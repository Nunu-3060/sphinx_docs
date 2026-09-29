import tkinter as tk
from tkinter import ttk

from PIL import ImageTk

from SandImage import SandImage


class FrameSand(ttk.Frame):
    def __init__(self, master: tk.Misc | None = None, sandimage: SandImage | None = None, interval: int = 10) -> None:
        super().__init__(master)
        if sandimage is None:
            sandimage = SandImage()
        self.sandimage: SandImage = sandimage
        self.image: ImageTk.PhotoImage = self.sandimage.image_tk()
        self.label: ttk.Label = ttk.Label(self, image=self.image)
        self.interval: int = interval
        self.label.pack()
        self.bind("<Destroy>", self._on_destroy)
        self._after_id: str | None = None
        self._after_id = self.after(self.interval, self.next)
        return None

    def next(self) -> None:
        self.sandimage.next()
        self.image = self.sandimage.image_tk()
        self.label.configure(image=self.image)
        self._after_id = self.after(self.interval, self.next)
        return None

    def _on_destroy(self, event: tk.Event) -> None:
        if event.widget is self and self._after_id is not None:
            self.after_cancel(self._after_id)
            self._after_id = None
        return None
