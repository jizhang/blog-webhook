from pathlib import Path

from typer import Typer
from PIL import Image

webp_cli = Typer()


@webp_cli.command()
def webp_convert(source: str):
    source_path = Path(source)
    if source_path.is_dir():
        for file_path in source_path.iterdir():
            convert_file(file_path)
    else:
        convert_file(source_path)


def convert_file(file_path: Path):
    if file_path.suffix.lower() == ".webp":
        print(f"Skip {file_path}")
        return

    with Image.open(file_path) as img:
        img.save(file_path.with_suffix(".webp"), "WEBP")
        print(f"Converted {file_path}")
