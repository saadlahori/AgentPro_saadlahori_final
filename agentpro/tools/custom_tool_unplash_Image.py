# Custom_Unsplash_Tool.py

# Imports
import os
from agentpro import ReactAgent
from agentpro.tools import Tool
from huggingface_hub import list_models
from typing import Any
from agentpro import create_model
import requests

from typing import Any, Optional, Dict
from pydantic import PrivateAttr
import requests

class UnsplashImageSearchTool(Tool):
    name: str = "Unsplash Image Search"
    description: str = "Fetches top 6 landscape images from Unsplash for a given keyword."
    action_type: str = "find_images_unsplash"
    input_format: str = "Search keyword as a string. Example: 'mountains'"

    _config: Dict[str, Any] = PrivateAttr()

    def __init__(self, api_key: Optional[str] = None, **data):
        super().__init__(**data)
        self._config = {
            "api_key": api_key or os.getenv("UNSPLASH_ACCESS_KEY")
        }

    def run(self, input_text: Any) -> str:
        if not isinstance(input_text, str):
            return "❌ Error: Expected a keyword string to search images."

        query = input_text.strip()
        if not query:
            return "❌ Error: Please provide a keyword to search for images."

        api_key = self._config.get("api_key")
        if not api_key:
            return "❌ Error: Unsplash API key is missing. Provide it during initialization or set 'UNSPLASH_ACCESS_KEY' in env."

        url = "https://api.unsplash.com/search/photos"
        params = {
            "query": query,
            "client_id": api_key,
            "orientation": "landscape",
            "per_page": 6
        }

        try:
            response = requests.get(url, params=params)
            if response.status_code != 200:
                return f"❌ Error {response.status_code}: {response.text}"

            data = response.json()
            results = data.get("results", [])
            if not results:
                return f"No images found for '{query}'."

            image_urls = [photo["urls"]["regular"] for photo in results]
            return "\n".join(image_urls)

        except requests.exceptions.RequestException as e:
            return f"❌ HTTP Request failed: {str(e)}"
        except Exception as e:
            return f"❌ Unexpected error: {str(e)}"
