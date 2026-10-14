"""Convert JPEG/PNG images to resized WebP and update references in notes/.

Usage: uv run optimize_images.py <file or directory>...

Images are resized to at most MAX_WIDTH pixels wide and stripped of metadata
(including GPS location). The original file is deleted once converted.
"""
import sys
from pathlib import Path

from PIL import Image, ImageOps

from builder.config import NOTES_DIR, ROOT_DIR

MAX_WIDTH = 1600
QUALITY = {'.jpg': 80, '.jpeg': 80, '.png': 90}


def optimize(path: Path) -> tuple[int, int]:
    output_path = path.with_suffix('.webp')
    with Image.open(path) as image:
        image = ImageOps.exif_transpose(image)
        if image.width > MAX_WIDTH:
            image = image.resize((MAX_WIDTH, round(image.height * MAX_WIDTH / image.width)), Image.LANCZOS)
        if image.mode not in ('RGB', 'RGBA'):
            has_alpha = 'A' in image.getbands() or 'transparency' in image.info
            image = image.convert('RGBA' if has_alpha else 'RGB')
        image.save(output_path, 'WEBP', quality=QUALITY[path.suffix.lower()], method=6)

    old_size, new_size = path.stat().st_size, output_path.stat().st_size
    path.unlink()
    return old_size, new_size


def update_references(old: Path, new: Path):
    old_url = '/' + old.relative_to(ROOT_DIR).as_posix()
    new_url = '/' + new.relative_to(ROOT_DIR).as_posix()
    for note in NOTES_DIR.rglob('*.md'):
        text = note.read_text(encoding='utf-8')
        if old_url in text:
            note.write_text(text.replace(old_url, new_url), encoding='utf-8')


def main():
    paths = []
    for arg in sys.argv[1:]:
        p = Path(arg).resolve()
        paths += sorted(p.rglob('*')) if p.is_dir() else [p]

    total_old = total_new = 0
    for path in paths:
        if path.suffix.lower() not in QUALITY:
            continue
        old_size, new_size = optimize(path)
        update_references(path, path.with_suffix('.webp'))
        total_old += old_size
        total_new += new_size
        print(f'{path.relative_to(ROOT_DIR)}: {old_size // 1024} KB -> {new_size // 1024} KB')

    if total_old:
        print(f'Total: {total_old // 1024} KB -> {total_new // 1024} KB')


if __name__ == '__main__':
    main()
