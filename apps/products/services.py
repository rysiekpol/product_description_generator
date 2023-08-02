from enum import Enum
from pathlib import Path
from typing import List, Optional

import requests
from django.conf import settings
from pydantic import BaseModel, Field, ValidationError


class Operation(Enum):
    CREATED = "created"
    UPDATED = "updated"


class ImaggaTagInfo(BaseModel):
    en: str


class ImaggaTag(BaseModel):
    tag: ImaggaTagInfo


class ImaggaResult(BaseModel):
    tags: List[ImaggaTag]


class ImaggaResponse(BaseModel):
    result: ImaggaResult


class ImaggaAPICredentials(BaseModel):
    api_key: str
    api_secret: str


class ImaggaAPIRequest(BaseModel):
    auth: ImaggaAPICredentials
    image_path: Path
    url: Optional[str] = Field(default="https://api.imagga.com/v2/tags")


class Product(BaseModel):
    name: str


class Message(BaseModel):
    role: str
    content: str = Field(default=None)


class GPTRequest(BaseModel):
    model: str = "gpt-3.5-turbo"
    messages: List[Message]
    max_tokens: int = 0
    n: int = 0


class OpenAIAPIRequest(BaseModel):
    product: Product
    tags: List[str]
    api_key: Optional[str] = Field(default=settings.GPT_API_KEY)
    endpoint: Optional[str] = Field(
        default="https://api.openai.com/v1/chat/completions"
    )

    @property
    def prompt(self) -> str:
        return f"Generate a product description for a {self.product.name} which has tags: {', '.join(self.tags)}"

    @property
    def headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }


class ResponseMessage(BaseModel):
    content: str


class ResponseChoice(BaseModel):
    message: ResponseMessage


class OpenAIResponse(BaseModel):
    choices: List[ResponseChoice]


def describe_product_images(product):
    api_key = settings.IMMAGA_API_KEY
    api_secret = settings.IMMAGA_API_SECRET
    combined_tags = set()
    for image in product.images.all():
        image_path = Path(settings.BASE_DIR, image.image.url.lstrip("/"))
        try:
            data = ImaggaAPIRequest(
                auth=ImaggaAPICredentials(api_key=api_key, api_secret=api_secret),
                image_path=image_path,
            )

            response = requests.post(
                data.url,
                auth=(data.auth.api_key, data.auth.api_secret),
                files={"image": open(data.image_path, "rb")},
            )
            response_data = response.json()

            parsed_response = ImaggaResponse.model_validate(response_data)

            # Extract the 3 most confident tags from the response
            tags = parsed_response.result.tags[:3]
            tag_names = [tag.tag.en for tag in tags]
        except requests.RequestException as e:
            return f"HTTP Request failed: {e}"
        except ValidationError as e:
            return f"Validation error: {e}"

        combined_tags.update(tag_names)
    return list(combined_tags)


def generate_product_description(product, tags, n, words):
    try:
        data = OpenAIAPIRequest(
            product=Product(name=product.name),
            tags=tags,
        )

        message = Message(role="user", content=data.prompt)

        gpt_request = GPTRequest(messages=[message], max_tokens=words, n=n)

        print(gpt_request.model_dump_json())
        response = requests.post(
            data.endpoint,
            json=gpt_request.model_dump(),
            headers=data.headers,
        )
        response_data = response.json()
        print(response_data)

        parsed_response = OpenAIResponse.model_validate(response_data)
        return parsed_response.choices[0].message.content.strip()
    except ValidationError as e:
        return f"Validation error: {e}"
    except requests.RequestException as e:
        return f"HTTP Request failed: {e}"
