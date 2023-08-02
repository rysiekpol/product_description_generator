from pathlib import Path

import requests
from django.conf import settings


def describe_product_images(product):
    api_key = settings.IMMAGA_API_KEY
    api_secret = settings.IMMAGA_API_SECRET
    combined_tags = set()
    for image in product.images.all():
        image_path = Path(settings.BASE_DIR, image.image.url.lstrip("/"))
        try:
            response = requests.post(
                "https://api.imagga.com/v2/tags",
                auth=(api_key, api_secret),
                files={"image": open(image_path, "rb")},
            )
            response_data = response.json()

            # Extract the 3 most confident tags from the response
            tags = response_data["result"]["tags"][:3]
            tag_names = [tag["tag"]["en"] for tag in tags]
        except requests.RequestException as e:
            return f"HTTP Request failed: {e}"

        combined_tags.update(tag_names)
    return list(combined_tags)


def generate_product_description(product, tags, n, words):
    api_key = settings.GPT_API_KEY
    endpoint = "https://api.openai.com/v1/chat/completions"

    prompt = f"Generate a product description for a {product.name} which has tags: {', '.join(tags)}"
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "max_tokens": words,
        "n": n,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    try:
        response = requests.post(endpoint, json=data, headers=headers)
        response_data = response.json()

        if "choices" in response_data and len(response_data["choices"]) > 0:
            return response_data["choices"][0]["message"]["content"].strip()
        else:
            return "Product description generation failed."

    except requests.RequestException as e:
        return f"HTTP Request failed: {e}"
