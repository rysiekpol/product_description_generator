import asyncio
import json

import aiohttp
from fastapi import FastAPI
from pydantic import BaseModel

from .services import translate_text

app = FastAPI()


class Data(BaseModel):
    text: str
    languages: list[str]
    n: int
    words: int


@app.get("/test/")
async def translate():
    return {"test": "test"}


@app.post("/translate/")
async def translate(
    data: Data,
):
    async with aiohttp.ClientSession() as session:
        tasks = [
            translate_text(data.text, lang, data.words, data.n, session)
            for lang in data.languages
        ]
        translations = await asyncio.gather(*tasks)

    translation_languages = json.dumps(translations)

    return translation_languages
