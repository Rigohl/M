from fastapi import APIRouter, HTTPException
from backend.utils.ai_integration import AIIntegration

router = APIRouter()
ai_client = AIIntegration(api_key="YOUR_API_KEY")

@router.post("/generate-text")
async def generate_text(prompt: str):
    result = ai_client.generate_text(prompt)
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.post("/generate-image")
async def generate_image(description: str):
    result = ai_client.generate_image(description)
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["error"])
    return result