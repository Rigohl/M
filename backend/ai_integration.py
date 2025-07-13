from typing import Any, Dict
from openai import OpenAI

class AIIntegration:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key)

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
