from fastapi import FastAPI, HTTPException, UploadFile, Request
from typing import Callable, Awaitable, Any
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from pydantic import BaseModel, ValidationError
from supabase import create_client
import asyncio
from backend.ai_integration import AIIntegration
from backend.routes.ai_routes import router as ai_router


# Configuración centralizada de Supabase y otras credenciales
from backend.config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# (Preparado para integración Suno)
SUNO_API_KEY = os.getenv("SUNO_API_KEY", "YOUR_SUNO_API_KEY")



# Configuración de CORS para permitir solo el frontend Next.js
origins = [
    "http://localhost:3000",  # Next.js local
    "https://tu-dominio-vercel.app"  # Producción, reemplaza por tu dominio real
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de logging estructurado
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logger = logging.getLogger("backend")

# Incluir rutas
app.include_router(ai_router, prefix="/ai")

# Inicializar cliente de AI Integration
ai_client = AIIntegration(api_key="YOUR_API_KEY")

# Modelos de datos


class SongCreationFormValues(BaseModel):
    title: str
    description: str
    genre: str

    @classmethod
    def validate_data(cls, data: dict[str, Any]) -> "SongCreationFormValues":
        return cls(**data)


class UserCredentials(BaseModel):
    email: str
    password: str

    @classmethod
    def validate_data(cls, data: dict[str, Any]) -> "UserCredentials":
        return cls(**data)


# Modelo de ejemplo para validación


class SongRequest(BaseModel):
    title: str
    artist: str
    genre: str


@app.middleware("http")
async def add_error_handling(request: Request, call_next: Callable[[Request], Awaitable[Any]]):
    try:
        response = await call_next(request)
        return response
    except ValidationError as ve:
        return JSONResponse(status_code=422, content={"detail": ve.errors()})
    except Exception as e:
        logger.error(f"Error inesperado: {e}", exc_info=True)
        return JSONResponse(
            status_code=500, content={"detail": "Internal Server Error"}
        )
# Endpoint de health check
@app.get("/health", tags=["infra"])
async def health_check():
    """Verifica que el backend está online y responde correctamente."""
    return {"status": "ok"}


# Endpoints


@app.post("/create-song", response_model=dict)
async def create_song(form_data: SongCreationFormValues):
    """
    Crea una canción usando IA a partir de los datos del formulario.
    - Valida y sanitiza los datos recibidos.
    - Devuelve letra y audio generado (simulado).
    """
    try:
        validated = SongCreationFormValues.validate_data(form_data.model_dump())
        # Simulación de generación de canción con IA
        await asyncio.sleep(3)
        return {
            "success": True,
            "lyrics": "Esta es una letra generada por IA para tu canción.",
            "audio": "/audio/placeholder.mp3",
        }
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/register-user", response_model=dict)
async def register_user(credentials: UserCredentials):
    """
    Registra un usuario en Supabase.
    - Valida y sanitiza los datos recibidos.
    - Maneja errores y devuelve el usuario creado.
    """
    try:
        validated = UserCredentials.validate_data(credentials.model_dump())
        response = supabase.auth.sign_up(
            {"email": validated.email, "password": validated.password}
        )
        error = response.__dict__.get("error")
        user = response.__dict__.get("user")
        if error:
            detail = error.get("message") if isinstance(error, dict) else str(error)
            raise HTTPException(status_code=400, detail=detail)
        return {"success": True, "user": user}
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/login-user", response_model=dict)
async def login_user(credentials: UserCredentials):
    """
    Inicia sesión de usuario en Supabase.
    - Valida y sanitiza los datos recibidos.
    - Maneja errores y devuelve el usuario autenticado.
    """
    try:
        validated = UserCredentials.validate_data(credentials.model_dump())
        response = supabase.auth.sign_in_with_password(
            {"email": validated.email, "password": validated.password}
        )
        error = response.__dict__.get("error")
        user = response.__dict__.get("user")
        if error:
            detail = error.get("message") if isinstance(error, dict) else str(error)
            raise HTTPException(status_code=400, detail=detail)
        return {"success": True, "user": user}
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


from pydantic import Field


class SongData(BaseModel):
    id: str = Field(..., min_length=1)
    title: str
    artist: str
    genre: str
    lyrics: str = ""
    audio_url: str = ""


@app.post("/save-song-data", response_model=dict)
async def save_song_data(song: SongData):
    """
    Guarda los datos de una canción en Supabase.
    - Valida y sanitiza los datos recibidos.
    - Maneja errores y devuelve confirmación.
    """
    try:
        validated = song.model_dump()
        response = supabase.table("songs").upsert(validated).execute()
        error = response.__dict__.get("error")
        if error:
            detail = error.get("message") if isinstance(error, dict) else str(error)
            raise HTTPException(status_code=400, detail=detail)
        return {"success": True}
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-album-art")
async def generate_album_art(description: str, style: str):
    try:
        # Simulación de generación de arte de álbum
        return {
            "success": True,
            "imageUrl": "https://placehold.co/600x600/333/FFF?text=Album+Art",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-cloned-voice")
async def generate_cloned_voice(audioFile: UploadFile):
    try:
        # Simulación de generación de voz clonada
        return {
            "success": True,
            "audioUrl": "https://placehold.co/audio/placeholder.mp3",
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
