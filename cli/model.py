from typer import Typer
from langchain.chat_models import init_chat_model

from app.settings import get_settings

model_cli = Typer()


@model_cli.command()
def model_translate(source: str):
    settings = get_settings()
    model = init_chat_model(
        base_url=settings.OPENAI_BASE_URL,
        api_key=settings.OPENAI_API_KEY,
        model="qwen3-max",
        model_provider="openai",
    )
    response = model.invoke("你是谁？")
    print(response)
