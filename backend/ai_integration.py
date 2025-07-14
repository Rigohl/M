from typing import Any, Dict
import openai

import os
import requests

class AIIntegration:
    def __init__(self, api_key: str):
        openai.api_key = api_key
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

    def generate_text(self, prompt: str, max_tokens: int = 100):
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens
            )
            content = None
            if response.choices and response.choices[0].message and response.choices[0].message.content:
                content = response.choices[0].message.content
            if content:
                return {"success": True, "data": content.strip()}
            else:
                return {"success": False, "error": "Respuesta vacía de OpenAI"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def generate_image(self, description: str):
        try:
            response = openai.images.generate(
                prompt=description,
                n=1,
                size="1024x1024"
            )
            url = None
            if hasattr(response, 'data') and response.data and hasattr(response.data[0], 'url'):
                url = response.data[0].url
            if url:
                return {"success": True, "data": url}
            else:
                return {"success": False, "error": "No se pudo obtener la URL de la imagen generada"}
        except Exception as e:
            return {"success": False, "error": str(e)}
