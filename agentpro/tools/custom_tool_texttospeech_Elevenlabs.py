# TextToSppech_Elevenlabs_Tool.py

import os
import json
import tempfile
import requests
from typing import Any, Optional, Dict
from pydantic import PrivateAttr, Field
from agentpro.tools import Tool

class TextToSpeechTool_ElevenLabsTTS(Tool):
    name: str = Field(default="Text to Speech ElevenLabs TTS")
    description: str = Field(default="Converts text into speech using ElevenLabs with custom voice and options.")
    action_type: str = Field(default="tts_elevenlabs")
    input_format: str = Field(
        default=(
            "JSON with keys: text (string), voice_id (string), model_id (optional), "
            "stability (float), similarity_boost (float)"
        )
    )

    _config: Dict[str, Any] = PrivateAttr()

    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self._config = {
            "api_key": api_key or os.getenv("ELEVENLABS_API_KEY")
        }
    def run(self, input_text: Any) -> str:
        try:
            data = input_text if isinstance(input_text, dict) else json.loads(input_text)
            text = data["text"].strip()
            model_id = data.get("model_id", "eleven_monolingual_v1")
            stability = float(data.get("stability", 0.75))
            similarity_boost = float(data.get("similarity_boost", 0.75))
        except Exception as e:
            return f"❌ Invalid input. Provide JSON with key: text. Optional: model_id, stability, similarity_boost. Error: {e}"

        if not text:
            return "❌ 'text' is a required field."

        # Hardcoded voice mapping
        voice_profiles = {
            "pNInz6obpgDQGcFmaJgB": {"name": "Adam", "gender": "Male"},
            "21m00Tcm4TlvDq8ikWAM": {"name": "Rachel", "gender": "Female"}
        }

        headers = {
            "xi-api-key": self._config["api_key"],
            "Content-Type": "application/json"
        }

        payload = {
            "text": text,
            "model_id": model_id,
            "voice_settings": {
                "stability": stability,
                "similarity_boost": similarity_boost
            }
        }

        messages = []
        for voice_id, meta in voice_profiles.items():
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            try:
                response = requests.post(url, json=payload, headers=headers)
                response.raise_for_status()

                if "audio" not in response.headers.get("content-type", ""):
                    messages.append(f"❌ {meta['name']} ({meta['gender']}, {voice_id}) returned no audio. Response: {response.text[:200]}")
                    continue

                base_name = "_".join(text.split()[:5]).replace("/", "_").replace("\\", "_")
                file_name = f"{meta['name']}_{base_name}.mp3"
                file_path = os.path.join(os.getcwd(), file_name)

                with open(file_path, "wb") as f:
                    f.write(response.content)

                messages.append(f"{file_name}; {meta['gender']}, {meta['name']}, {voice_id}")

            except Exception as e:
                messages.append(f"❌ Failed for {meta['name']} ({voice_id}): {e}")

        return "\n".join(messages)


    # def run(self, input_text: Any) -> str:
    #     try:
    #         data = input_text if isinstance(input_text, dict) else json.loads(input_text)
    #         text = data["text"].strip()
    #         voice_id = data["voice_id"]
    #         model_id = data.get("model_id", "eleven_monolingual_v1")
    #         stability = float(data.get("stability", 0.75))
    #         similarity_boost = float(data.get("similarity_boost", 0.75))
    #     except Exception as e:
    #         return f"❌ Invalid input. Provide JSON with keys: text, voice_id. Optional: model_id, stability, similarity_boost. Error: {e}"

    #     if not text or not voice_id:
    #         return "❌ 'text' and 'voice_id' are required fields."

    #     headers = {
    #         "xi-api-key": self._config["api_key"],
    #         "Content-Type": "application/json"
    #     }
    #     url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    #     payload = {
    #         "text": text,
    #         "model_id": model_id,
    #         "voice_settings": {
    #             "stability": stability,
    #             "similarity_boost": similarity_boost
    #         }
    #     }
    #     try:
    #         response = requests.post(url, json=payload, headers=headers)
    #         response.raise_for_status()

    #         if "audio" not in response.headers.get("content-type", ""):
    #             return f"❌ API did not return audio. Response: {response.text[:200]}"

    #         # Generate a safe filename from the input text
    #         filename = "_".join(text.split()[:5]) + ".mp3"
    #         filename = filename.replace("/", "_").replace("\\", "_")
    #         file_path = os.path.join(os.getcwd(), filename)

    #         with open(file_path, "wb") as f:
    #             f.write(response.content)

    #         return f"✅ Speech generated and saved to `{filename}`. This is an `.mp3` file and will be playable below."

    #     except Exception as e:
    #         return f"❌ Failed to generate speech: {e}"

        # try:
        #     response = requests.post(url, json=payload, headers=headers)
        #     response.raise_for_status()

        #     if "audio" not in response.headers.get("content-type", ""):
        #         return f"❌ API did not return audio. Response: {response.text[:200]}"

        #     with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        #         f.write(response.content)
        #         return f.name  # return path to audio file

        # except Exception as e:
        #     return f"❌ Failed to generate speech: {e}"
