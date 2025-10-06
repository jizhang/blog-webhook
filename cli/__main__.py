from typer import Typer
from .webp import webp_cli

cli = Typer()
cli.add_typer(webp_cli)

cli()
