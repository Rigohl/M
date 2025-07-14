#!/usr/bin/env python3
"""
Módulo de gestión de errores para aplicaciones Python
Proporciona clases y utilidades para manejar errores de forma consistente
"""

import logging
import sys
import traceback
from typing import Any, Dict, Optional, Type, Union, List, Callable
from functools import wraps

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger("ErrorHandler")


class AppError(Exception):
    """
    Excepción base para errores de la aplicación

    Atributos:
        message (str): Mensaje de error
        status_code (int): Código de estado HTTP
        error_code (str): Código de error interno
        details (dict): Detalles adicionales del error
    """

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: str = "INTERNAL_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ):
        """
        Inicializa la excepción

        Args:
            message: Mensaje descriptivo del error
            status_code: Código de estado HTTP (por defecto 500)
            error_code: Código de error interno
            details: Información adicional sobre el error
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte la excepción a un diccionario

        Returns:
            Diccionario con la información del error
        """
        return {
            "error": True,
            "message": self.message,
            "statusCode": self.status_code,
            "errorCode": self.error_code,
            "details": self.details,
        }


class ValidationError(AppError):
    """Excepción para errores de validación"""

    def __init__(
        self,
        message: str,
        field: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        """
        Inicializa la excepción

        Args:
            message: Mensaje descriptivo del error
            field: Campo que falló la validación
            details: Información adicional sobre el error
        """
        super().__init__(
            message=message,
            status_code=400,
            error_code="VALIDATION_ERROR",
            details=details or {},
        )
        if field:
            self.details["field"] = field


class NotFoundError(AppError):
    """Excepción para recursos no encontrados"""

    def __init__(
        self,
        resource_type: str,
        resource_id: Optional[Union[str, int]] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        """
        Inicializa la excepción

        Args:
            resource_type: Tipo de recurso no encontrado (usuario, producto, etc.)
            resource_id: Identificador del recurso
            details: Información adicional sobre el error
        """
        message = f"{resource_type} no encontrado"
        if resource_id:
            message = f"{resource_type} con ID {resource_id} no encontrado"

        super().__init__(
            message=message,
            status_code=404,
            error_code="NOT_FOUND",
            details=details or {},
        )
        self.details["resourceType"] = resource_type
        if resource_id:
            self.details["resourceId"] = resource_id


class AuthenticationError(AppError):
    """Excepción para errores de autenticación"""

    def __init__(
        self,
        message: str = "Error de autenticación",
        details: Optional[Dict[str, Any]] = None,
    ):
        """
        Inicializa la excepción

        Args:
            message: Mensaje descriptivo del error
            details: Información adicional sobre el error
        """
        super().__init__(
            message=message,
            status_code=401,
            error_code="AUTHENTICATION_ERROR",
            details=details or {},
        )


class AuthorizationError(AppError):
    """Excepción para errores de autorización"""

    def __init__(
        self,
        message: str = "No tiene permiso para realizar esta acción",
        details: Optional[Dict[str, Any]] = None,
    ):
        """
        Inicializa la excepción

        Args:
            message: Mensaje descriptivo del error
            details: Información adicional sobre el error
        """
        super().__init__(
            message=message,
            status_code=403,
            error_code="AUTHORIZATION_ERROR",
            details=details or {},
        )


class ErrorHandler:
    """
    Clase para manejar errores de forma centralizada

    Esta clase proporciona métodos para manejar diferentes tipos de errores
    y convertirlos en respuestas HTTP estandarizadas.
    """

    @staticmethod
    def handle_exception(exc: Exception) -> Dict[str, Any]:
        """
        Maneja una excepción y la convierte en una respuesta

        Args:
            exc: Excepción a manejar

        Returns:
            Diccionario con la respuesta de error
        """
        if isinstance(exc, AppError):
            return exc.to_dict()

        # Excepción no controlada
        logger.error(f"Error no controlado: {str(exc)}")
        logger.error(traceback.format_exc())

        return {
            "error": True,
            "message": "Error interno del servidor",
            "statusCode": 500,
            "errorCode": "INTERNAL_ERROR",
            "details": {"originalError": str(exc)},
        }

    @staticmethod
    def handle_error(
        status_code: int,
        message: str,
        error_code: str = "ERROR",
        details: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Crea una respuesta de error

        Args:
            status_code: Código de estado HTTP
            message: Mensaje descriptivo del error
            error_code: Código de error interno
            details: Información adicional sobre el error

        Returns:
            Diccionario con la respuesta de error
        """
        return {
            "error": True,
            "message": message,
            "statusCode": status_code,
            "errorCode": error_code,
            "details": details or {},
        }


def error_handler(func: Callable) -> Callable:
    """
    Decorador para manejar errores en funciones

    Args:
        func: Función a decorar

    Returns:
        Función decorada
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return ErrorHandler.handle_exception(e)

    return wrapper
