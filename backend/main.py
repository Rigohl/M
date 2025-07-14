from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from datetime import datetime, timedelta, timezone
# Configuración JWT
JWT_SECRET = os.getenv("JWT_SECRET", "supersecretkey")
JWT_ALGORITHM = "HS256"
security = HTTPBearer()

def create_jwt_token(data: dict, expires_delta: int = 60*24):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    # Si no hay rol, asignar 'user' por defecto
    if "role" not in to_encode:
        to_encode["role"] = "user"
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
from fastapi import FastAPI, HTTPException, UploadFile, Request
from pydantic import Field
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
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("backend")
    ]
)
logger = logging.getLogger("backend")

# Incluir rutas
app.include_router(ai_router, prefix="/ai")

# Inicializar cliente de AI Integration
ai_client = AIIntegration(api_key="YOUR_API_KEY")


# --- Monetización y control de canciones ---
from typing import Optional

# Simulación de planes y precios
PLANES = {
    "paquete1": {"precio": 149, "canciones": 1},
    "paquete2": {"precio": 399, "canciones": 3},
}


from typing import Dict, List, Any, Optional, Callable, Awaitable, TypeVar, cast
USERS_DB: Dict[str, Dict[str, Any]] = {}
# Auditoría en memoria
PURCHASE_HISTORY: List[Dict[str, Any]] = []  # [{'email': ..., 'plan': ..., 'timestamp': ...}]
SONG_HISTORY: List[Dict[str, Any]] = []      # [{'email': ..., 'title': ..., 'timestamp': ...}]

def get_user(email: str) -> Dict[str, Any]:
    if email not in USERS_DB:
        USERS_DB[email] = {"plan": None, "canciones_restantes": 0}
    return USERS_DB[email]

def can_create_song(email: str) -> bool:
    user: Dict[str, Any] = get_user(email)
    return int(user.get("canciones_restantes", 0)) > 0

def decrement_song(email: str) -> None:
    user: Dict[str, Any] = get_user(email)
    if int(user.get("canciones_restantes", 0)) > 0:
        user["canciones_restantes"] -= 1

def assign_plan(email: str, plan: str) -> bool:
    if plan in PLANES:
        USERS_DB[email] = {"plan": plan, "canciones_restantes": PLANES[plan]["canciones"]}
        # Registrar compra en historial
        PURCHASE_HISTORY.append({
            "email": email,
            "plan": plan,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        return True
    return False


class SongCreationFormValues(BaseModel):
    """
    Datos requeridos para crear una canción con IA.
    """
    title: str = Field(..., description="Título de la canción")
    description: str = Field(..., description="Descripción o tema de la canción")
    genre: str = Field(..., description="Género musical")

    @classmethod
    def validate_data(cls, data: dict[str, Any]) -> "SongCreationFormValues":
        return cls(**data)


class UserCredentials(BaseModel):
    """
    Credenciales de usuario para registro y login.
    """
    email: str = Field(..., description="Correo electrónico")
    password: str = Field(..., description="Contraseña")

    @classmethod
    def validate_data(cls, data: dict[str, Any]) -> "UserCredentials":
        return cls(**data)


# Modelo de ejemplo para validación


class SongRequest(BaseModel):
    """
    Modelo de ejemplo para validación de canciones.
    """
    title: str = Field(...)
    artist: str = Field(...)
    genre: str = Field(...)


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
async def create_song(form_data: SongCreationFormValues) -> Dict[str, Any]:
    """
    Crea una canción usando IA a partir de los datos del formulario.
    - Valida y sanitiza los datos recibidos.
    - Devuelve letra y audio generado (simulado).
    """
    validated = SongCreationFormValues.validate_data(form_data.model_dump())
    # Obtener usuario autenticado por JWT
    from fastapi import Depends
    from fastapi.security import HTTPAuthorizationCredentials
    request: Optional[Any] = None
    import inspect
    for frame in inspect.stack():
        if "request" in frame.frame.f_locals:
            request = frame.frame.f_locals["request"]
            break
    token: Optional[str] = None
    if request and hasattr(request, "headers") and "authorization" in request.headers:
        token = request.headers["authorization"].split()[1]
    email: Optional[str] = None
    if token:
        payload = verify_jwt_token(token)
        email = payload.get("sub") if payload else None
    if not email:
        raise HTTPException(status_code=401, detail="No autenticado")
    if not can_create_song(email):
        raise HTTPException(status_code=402, detail="No tienes canciones disponibles. Compra un paquete.")
    decrement_song(email)
    # Registrar generación de canción en historial
    SONG_HISTORY.append({
        "email": email,
        "title": validated.title,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })
    # Simulación de generación de canción con IA
    await asyncio.sleep(3)
    return {
        "success": True,
        "lyrics": "Esta es una letra generada por IA para tu canción.",
        "audio": "/audio/placeholder.mp3",
        "canciones_restantes": get_user(email)["canciones_restantes"]
    }
# Endpoint para comprar paquete
@app.post("/comprar-paquete", tags=["Pagos"])
from fastapi import Depends
@app.post("/comprar-paquete", tags=["Pagos"])
def comprar_paquete(plan: str, credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    payload = verify_jwt_token(credentials.credentials)
    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="No autenticado")
    if assign_plan(email, plan):
        return {"success": True, "plan": plan, "canciones_restantes": get_user(email)["canciones_restantes"]}
    else:
        raise HTTPException(status_code=400, detail="Plan inválido")


@app.post("/register-user", response_model=dict)
async def register_user(credentials: UserCredentials) -> Dict[str, Any]:
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
        error: Optional[Any] = response.__dict__.get("error")
        user: Optional[Any] = response.__dict__.get("user")
        if error:
            detail: str = error["message"] if isinstance(error, dict) and "message" in error else str(error)
            raise HTTPException(status_code=400, detail=detail)
        return {"success": True, "user": user}
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/login-user", response_model=dict)
async def login_user(credentials: UserCredentials) -> Dict[str, Any]:
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
        error: Optional[Any] = response.__dict__.get("error")
        user: Optional[Any] = response.__dict__.get("user")
        if error:
            detail: str = error["message"] if isinstance(error, dict) and "message" in error else str(error)
            raise HTTPException(status_code=400, detail=detail)
        # Generar token JWT al hacer login
        user_email: Optional[str] = None
        if user:
            if isinstance(user, dict):
                user_email = user.get("email")
            else:
                user_email = getattr(user, "email", None)
        if not user_email:
            raise HTTPException(status_code=400, detail="Usuario inválido")
        # Ejemplo: si el email es admin@, asignar rol admin
        role: str = "admin" if user_email.startswith("admin@") else "user"
        token: str = create_jwt_token({"sub": user_email, "role": role})
        return {"success": True, "user": user, "token": token, "role": role}
# Endpoint protegido de ejemplo
from fastapi import Depends

@app.get("/protected", tags=["Seguridad"])
def protected_route(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    try:
        payload = verify_jwt_token(credentials.credentials)
        return {"message": f"Acceso permitido para {payload['sub']}", "role": payload.get("role", "user")}
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint solo para admin
# Endpoint solo para admin

# Decorador para endpoints admin
from functools import wraps
from fastapi import Request
F = TypeVar("F", bound=Callable[..., Awaitable[Any]])
def admin_required(func: F) -> F:
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        request: Optional[Request] = kwargs.get('request')
        credentials: Optional[HTTPAuthorizationCredentials] = kwargs.get('credentials')
        if not credentials:
            # Buscar en args
            for arg in args:
                if isinstance(arg, HTTPAuthorizationCredentials):
                    credentials = arg
        if not credentials:
            raise HTTPException(status_code=401, detail="No autenticado")
        payload: Dict[str, Any] = verify_jwt_token(credentials.credentials)
        if payload.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Solo administradores")
        return await func(*args, **kwargs)
    return cast(F, wrapper)

@app.get("/admin-only", tags=["Seguridad"])
@admin_required
async def admin_only(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    payload = verify_jwt_token(credentials.credentials)
    return {"message": f"Acceso admin permitido para {payload['sub']}"}

# --- Endpoints de administración y auditoría ---

@app.get("/admin/ventas", tags=["Admin"])
@admin_required
async def admin_ventas(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Devuelve el total de ventas y detalle de compras."""
    total_ventas = sum(PLANES[compra['plan']]['precio'] for compra in PURCHASE_HISTORY)
    return {
        "total_ventas": total_ventas,
        "compras": PURCHASE_HISTORY
    }

@app.get("/admin/canciones", tags=["Admin"])
@admin_required
async def admin_canciones(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Devuelve el total de canciones generadas y detalle."""
    return {
        "total_canciones": len(SONG_HISTORY),
        "canciones": SONG_HISTORY
    }

@app.get("/admin/usuarios", tags=["Admin"])
@admin_required
async def admin_usuarios(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Devuelve la lista de usuarios activos (que han comprado o generado canciones)."""
    usuarios_compras = {c['email'] for c in PURCHASE_HISTORY}
    usuarios_canciones = {c['email'] for c in SONG_HISTORY}
    usuarios = list(usuarios_compras.union(usuarios_canciones))
    return {"usuarios_activos": usuarios, "total": len(usuarios)}

@app.get("/admin/historial-compras", tags=["Admin"])
@admin_required
async def admin_historial_compras(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Devuelve el historial completo de compras."""
    return {"historial_compras": PURCHASE_HISTORY}

@app.get("/admin/historial-canciones", tags=["Admin"])
@admin_required
async def admin_historial_canciones(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Devuelve el historial completo de canciones generadas."""
    return {"historial_canciones": SONG_HISTORY}


from pydantic import Field


class SongData(BaseModel):
    """
    Datos completos de una canción almacenada.
    """
    id: str = Field(..., min_length=1, description="ID único de la canción")
    title: str = Field(..., description="Título de la canción")
    artist: str = Field(..., description="Artista")
    genre: str = Field(..., description="Género musical")
    lyrics: str = Field("", description="Letra de la canción")
    audio_url: str = Field("", description="URL del audio generado")


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
