from typer import Typer
from .webp import webp_cli
from .model import model_cli

cli = Typer()
cli.add_typer(webp_cli)
cli.add_typer(model_cli)

cli()
