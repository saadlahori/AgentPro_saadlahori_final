# Imports
import os
from agentpro import ReactAgent
from agentpro.tools import Tool
from huggingface_hub import list_models
from typing import Any
from agentpro import create_model

import requests
from typing import Any

UNSPLASH_ACCESS_KEY = "your_unsplash_access_key_here"  # Replace with your real key

class UnsplashImageTool(Tool):
    name: str = "Image Finder from Unsplash"
    description: str = "Fetches a photo URL from Unsplash for a given search category or keyword."
    action_type: str = "find_image_unsplash"
    input_format: str = "Search keyword as a string. Example: 'nature'"

    def run(self, input_text: Any) -> str:
        query = input_text.strip()
        url = "https://api.unsplash.com/photos/random"
        params = {
            "query": query,
            "client_id": UNSPLASH_ACCESS_KEY,
            "orientation": "landscape"
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data["urls"]["regular"]  # or "full", "thumb", etc.
        else:
            return f"Error: {response.status_code} - {response.text}"
