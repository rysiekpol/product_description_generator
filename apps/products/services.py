from enum import Enum
from pathlib import Path, PosixPath
from typing import List, Optional

import requests
from django.conf import settings
from pydantic import BaseModel, Field, ValidationError


class Operation(Enum):
    CREATED = "created"
    UPDATED = "updated"


class ImaggaAPICredentials(BaseModel):
    api_key: str
    api_secret: str


class ImaggaAPIRequest(BaseModel):
    auth: ImaggaAPICredentials
    image_path: Path
    url: Optional[str] = Field(default="https://api.imagga.com/v2/tags")


class Product(BaseModel):
    name: str


class OpenAIAPIRequest(BaseModel):
    product: Product
    tags: List[str]
    n: int
    words: int
    api_key: Optional[str] = Field(default=settings.GPT_API_KEY)
    endpoint: Optional[str] = Field(
        default="https://api.openai.com/v1/chat/completions"
    )

    @property
    def prompt(self) -> str:
        return f"Generate a product description for a {self.product.name} which has tags: {', '.join(self.tags)}"

    @property
    def data(self) -> dict:
        return {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": self.prompt,
                }
            ],
            "max_tokens": self.words,
            "n": self.n,
        }

    @property
    def headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }


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

            # Extract the 3 most confident tags from the response
            tags = response_data["result"]["tags"][:3]
            tag_names = [tag["tag"]["en"] for tag in tags]
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
            n=n,
            words=words,
        )

        response = requests.post(data.endpoint, json=data.data, headers=data.headers)
        response_data = response.json()

        if "choices" in response_data and len(response_data["choices"]) > 0:
            return response_data["choices"][0]["message"]["content"].strip()
        else:
            return False
    except ValidationError as e:
        return e
    except requests.RequestException as e:
        return e
