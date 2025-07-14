from typing import Any, Dict
from openai import OpenAI

import os
import requests

class AIIntegration:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key)

        # Integración Suno
        self.suno_api_key = os.getenv("SUNO_API_KEY", "YOUR_SUNO_API_KEY")
        self.suno_base_url = os.getenv("SUNO_API_URL", "https://api.suno.ai/v1")

    def generate_song_suno(self, prompt: str, style: str = "pop", timeout: int = 30):
        """
        Genera una canción usando la API de Suno (API Box)
        Args:
            prompt (str): Descripción o letra base
            style (str): Estilo musical
            timeout (int): Timeout en segundos
        Returns:
            dict: Respuesta de la API Suno
        """
        headers = {
            "Authorization": f"Bearer {self.suno_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "prompt": prompt,
            "style": style
        }
        try:
            response = requests.post(
                f"{self.suno_base_url}/generate-song",
                headers=headers,
                json=payload,
                timeout=timeout
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.Timeout:
            return {"success": False, "error": "Timeout al conectar con Suno"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def generate_text(self, prompt: str, max_tokens: int = 100) -> Dict[str, Any]:
        try:
            response = self.client.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=max_tokens
            )
            return {"success": True, "data": response.choices[0].text.strip()}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def generate_image(self, description: str) -> Dict[str, Any]:
        try:
            response = self.client.Image.create(
                prompt=description,
                n=1,
                size="1024x1024"
            )
            return {"success": True, "data": response.data[0].url}
        except Exception as e:
            return {"success": False, "error": str(e)}
