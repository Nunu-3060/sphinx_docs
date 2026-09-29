from pathlib import Path

from SandImage import SandImage


def main() -> None:
    pixel: int = 4
    width: int = 1920 // pixel
    height: int = 1080 // pixel
    si: SandImage = SandImage(width=width, height=height, pixel=pixel)
    for _ in range(256):
        si.next()
    si.image_pil().save(Path(__file__).resolve().with_suffix(".png"))
    return None


if __name__ == "__main__":
    main()
