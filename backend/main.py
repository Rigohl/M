from fastapi import FastAPI, HTTPException, UploadFile, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
from supabase import create_client
from datadog import initialize, statsd
import asyncio
from backend.ai_integration import AIIntegration
from backend.routes.ai_routes import router as ai_router


# Configuración centralizada de Supabase y otras credenciales
from backend.config import SUPABASE_URL, SUPABASE_KEY
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# (Preparado para integración Suno)
SUNO_API_KEY = os.getenv("SUNO_API_KEY", "YOUR_SUNO_API_KEY")

# Configuración de Datadog
options = {
    'api_key': 'YOUR_DATADOG_API_KEY',
    'app_key': 'YOUR_DATADOG_APP_KEY'
}
initialize(**options)

# Inicializar FastAPI
app = FastAPI()

# Incluir rutas
app.include_router(ai_router, prefix="/ai")

# Inicializar cliente de AI Integration
ai_client = AIIntegration(api_key="YOUR_API_KEY")

# Modelos de datos
class SongCreationFormValues(BaseModel):
    title: str
    description: str
    genre: str

class UserCredentials(BaseModel):
    email: str
    password: str

# Modelo de ejemplo para validación
class SongRequest(BaseModel):
    title: str
    artist: str
    genre: str

# Middleware para manejo de errores
@app.middleware("http")
async def add_error_handling(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except ValidationError as ve:
        return JSONResponse(status_code=422, content={"detail": ve.errors()})
    except Exception as e:
        statsd.increment("backend.errors", tags=["error_type:exception"])
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

# Endpoints
@app.post("/create-song")
async def create_song(form_data: SongCreationFormValues):
    try:
        # Simulación de generación de canción con IA
        await asyncio.sleep(3)
        return {
            "success": True,
            "lyrics": "Esta es una letra generada por IA para tu canción.",
            "audio": "/audio/placeholder.mp3"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/register-user")
async def register_user(credentials: UserCredentials):
    try:
        response = supabase.auth.sign_up({"email": credentials.email, "password": credentials.password})
        if response.get("error"):
            raise HTTPException(status_code=400, detail=response["error"]["message"])
        return {"success": True, "user": response["user"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/login-user")
async def login_user(credentials: UserCredentials):
    try:
        response = supabase.auth.sign_in_with_password({"email": credentials.email, "password": credentials.password})
        if response.get("error"):
            raise HTTPException(status_code=400, detail=response["error"]["message"])
        return {"success": True, "user": response["user"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/save-song-data")
async def save_song_data(song_id: str, song_data: dict):
    try:
        response = supabase.table("songs").upsert({"id": song_id, **song_data}).execute()
        if response.get("error"):
            raise HTTPException(status_code=400, detail=response["error"]["message"])
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-album-art")
async def generate_album_art(description: str, style: str):
    try:
        # Simulación de generación de arte de álbum
        return {
            "success": True,
            "imageUrl": "https://placehold.co/600x600/333/FFF?text=Album+Art"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-cloned-voice")
async def generate_cloned_voice(audioFile: UploadFile):
    try:
        # Simulación de generación de voz clonada
        return {
            "success": True,
            "audioUrl": "https://placehold.co/audio/placeholder.mp3"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-text")
async def generate_text(prompt: str):
    try:
        result = ai_client.generate_text(prompt)
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-image")
async def generate_image(description: str):
    try:
        result = ai_client.generate_image(description)
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
