from typer import Typer

model_cli = Typer()

from . import translate

__all__ = ["model_cli"]
