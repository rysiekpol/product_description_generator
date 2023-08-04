import asyncio
import os
from typing import List, Optional

import aiohttp
from pydantic import BaseModel, Field, ValidationError


class ResponseMessage(BaseModel):
    content: str


class ResponseChoice(BaseModel):
    message: ResponseMessage


class OpenAIResponse(BaseModel):
    choices: List[ResponseChoice]


class OpenAIResponse(BaseModel):
    choices: List[ResponseChoice]


class Message(BaseModel):
    role: str
    content: str = Field(default=None)


class GPTRequest(BaseModel):
    model: str = "gpt-3.5-turbo"
    messages: List[Message]
    max_tokens: int = 0
    n: int = 0


class TranslationRequest(BaseModel):
    api_key: Optional[str] = Field(default=os.environ.get("GPT_API_KEY"))
    endpoint: Optional[str] = Field(
        default="https://api.openai.com/v1/chat/completions"
    )
    language: str
    text: str

    @property
    def prompt(self) -> str:
        return (
            f"Translate the following text from English to {self.language}: {self.text}"
        )

    @property
    def headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }


async def translate_text(text: str, target_language: str, words: int, n: int, session):
    try:
        translation_request = TranslationRequest(language=target_language, text=text)
        message = Message(role="user", content=translation_request.prompt)

        gpt_request = GPTRequest(messages=[message], max_tokens=words, n=n)

        async with session.post(
            translation_request.endpoint,
            json=gpt_request.model_dump(),
            headers=translation_request.headers,
        ) as response:
            response_data = await response.json()

        parsed_response = OpenAIResponse.model_validate(response_data)
        return {target_language: parsed_response.choices[0].message.content.strip()}
    except ValidationError as e:
        return e
