from datetime import datetime
from pathlib import Path

from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate

from . import model_cli, prompts
from app.settings import get_settings


@model_cli.command()
def model_translate(source: str):
    settings = get_settings()

    source_path = Path(source)
    with source_path.open() as f:
        blog_content = f.read()

    prompt_template = PromptTemplate.from_template(prompts.TRANSLATE_PROMPT)
    prompt = prompt_template.format(
        current_date=datetime.now().strftime('%Y-%m-%d'),
        blog_content=blog_content,
    )

    model = init_chat_model(
        base_url=settings.OPENAI_BASE_URL,
        api_key=settings.OPENAI_API_KEY,
        model="qwen3-max",
        model_provider="openai",
    )
    response = model.invoke(prompt)

    target_path = source_path.with_suffix(".zh.md")
    with target_path.open("w") as f:
        f.write(response.content)
    print(f"Written to {target_path}")
