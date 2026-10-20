"""Render the captured terminal transcript as a clean evidence image."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "evidence" / "padding-oracle-demo.txt"
TARGET = ROOT / "assets" / "padding-oracle-evidence.png"
FONT = r"C:\Windows\Fonts\CascadiaMono.ttf"
FONT_BOLD = r"C:\Windows\Fonts\CascadiaMono.ttf"


def color_for(line: str) -> str:
    if line.startswith("=="):
        return "#7dd3fc"
    if line.startswith("RESULT:") or "after forgery" in line:
        return "#86efac"
    if "invalid padding" in line:
        return "#fca5a5"
    if "oracle queries" in line or "recovered plaintext" in line:
        return "#fde68a"
    return "#d6deeb"


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8").rstrip()
    font = ImageFont.truetype(FONT, 21)
    title_font = ImageFont.truetype(FONT_BOLD, 21)

    width = 1720
    padding = 34
    title_height = 58
    line_height = 30
    lines = text.splitlines()
    height = title_height + padding * 2 + line_height * (len(lines) + 2)
    image = Image.new("RGB", (width, height), "#0b1220")
    draw = ImageDraw.Draw(image)

    draw.rectangle((0, 0, width, title_height), fill="#111827")
    for index, color in enumerate(("#ff5f56", "#ffbd2e", "#27c93f")):
        left = 22 + index * 26
        draw.ellipse((left, 17, left + 14, 31), fill=color)
    draw.text(
        (118, 16),
        "Padding-oracle lab - localhost evidence",
        font=title_font,
        fill="#f8fafc",
    )

    y = title_height + padding
    draw.text((padding, y), "PS> python scripts/run_demo.py", font=title_font, fill="#86efac")
    y += line_height + 8

    for line in lines:
        draw.text((padding, y), line, font=font, fill=color_for(line))
        y += line_height

    TARGET.parent.mkdir(parents=True, exist_ok=True)
    image.save(TARGET, "PNG", optimize=True)
    print(f"Wrote {TARGET} ({width}x{height})")


if __name__ == "__main__":
    main()
