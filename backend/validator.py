#!/usr/bin/env python3
"""
Módulo de validación de datos
Proporciona utilidades para validar datos de entrada
"""

import re
import uuid
from typing import Any, Dict, List, Optional, Type, TypeVar, Union, Callable, cast
from datetime import datetime
from error_handler import ValidationError

T = TypeVar('T')


class Validator:
    """
    Clase para validar datos de entrada
    
    Esta clase proporciona métodos para validar diferentes tipos de datos
    y lanzar excepciones de validación cuando los datos no son válidos.
    """
    
    @staticmethod
    def validate_required(value: Any, field_name: str) -> None:
        """
        Valida que un campo requerido tenga un valor
        
        Args:
            value: Valor a validar
            field_name: Nombre del campo
            
        Raises:
            ValidationError: Si el valor es None o cadena vacía
        """
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValidationError(f"El campo {field_name} es obligatorio", field=field_name)
    
    @staticmethod
    def validate_string(value: Any, field_name: str, min_length: int = 0, max_length: Optional[int] = None) -> str:
        """
        Valida que un valor sea una cadena con longitud dentro del rango
        
        Args:
            value: Valor a validar
            field_name: Nombre del campo
            min_length: Longitud mínima (por defecto 0)
            max_length: Longitud máxima (por defecto None)
            
        Returns:
            Cadena validada
            
        Raises:
            ValidationError: Si el valor no es una cadena o está fuera del rango
        """
        if not isinstance(value, str):
            raise ValidationError(f"El campo {field_name} debe ser una cadena", field=field_name)
        
        value = value.strip()
        
        if len(value) < min_length:
            raise ValidationError(
                f"El campo {field_name} debe tener al menos {min_length} caracteres",
                field=field_name
            )
        
        if max_length is not None and len(value) > max_length:
            raise ValidationError(
                f"El campo {field_name} debe tener como máximo {max_length} caracteres",
                field=field_name
            )
        
        return value
    
    @staticmethod
    def validate_integer(
        value: Any,
        field_name: str,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None
    ) -> int:
        """
        Valida que un valor sea un entero dentro del rango
        
        Args:
            value: Valor a validar
            field_name: Nombre del campo
            min_value: Valor mínimo (por defecto None)
            max_value: Valor máximo (por defecto None)
            
        Returns:
            Entero validado
            
        Raises:
            ValidationError: Si el valor no es un entero o está fuera del rango
        """
        if value is None:
            raise ValidationError(f"El campo {field_name} es obligatorio", field=field_name)
        
        try:
            int_value = int(value)
        except (ValueError, TypeError):
            raise ValidationError(f"El campo {field_name} debe ser un número entero", field=field_name)
        
        if min_value is not None and int_value < min_value:
            raise ValidationError(
                f"El campo {field_name} debe ser mayor o igual a {min_value}",
                field=field_name
            )
        
        if max_value is not None and int_value > max_value:
            raise ValidationError(
                f"El campo {field_name} debe ser menor o igual a {max_value}",
                field=field_name
            )
        
        return int_value
    
    @staticmethod
    def validate_float(
        value: Any,
        field_name: str,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None
    ) -> float:
        """
        Valida que un valor sea un número de punto flotante dentro del rango
        
        Args:
            value: Valor a validar
            field_name: Nombre del campo
            min_value: Valor mínimo (por defecto None)
            max_value: Valor máximo (por defecto None)
            
        Returns:
            Flotante validado
            
        Raises:
            ValidationError: Si el valor no es un flotante o está fuera del rango
        """
        if value is None:
            raise ValidationError(f"El campo {field_name} es obligatorio", field=field_name)
        
        try:
            float_value = float(value)
        except (ValueError, TypeError):
            raise ValidationError(f"El campo {field_name} debe ser un número", field=field_name)
        
        if min_value is not None and float_value < min_value:
            raise ValidationError(
                f"El campo {field_name} debe ser mayor o igual a {min_value}",
                field=field_name
            )
        
        if max_value is not None and float_value > max_value:
            raise ValidationError(
                f"El campo {field_name} debe ser menor o igual a {max_value}",
                field=field_name
            )
        
        return float_value
    
    @staticmethod
    def validate_email(value: Any, field_name: str) -> str:
        """
        Valida que un valor sea una dirección de correo electrónico válida
        
        Args:
            value: Valor a validar
            field_name: Nombre del campo
            
        Returns:
            Correo electrónico validado
            
        Raises:
            ValidationError: Si el valor no es un correo electrónico válido
        """
        if not isinstance(value, str):
            raise ValidationError(f"El campo {field_name} debe ser una cadena", field=field_name)
        
        value = value.strip().lower()
        
        if not value:
            raise ValidationError(f"El campo {field_name} es obligatorio", field=field_name)
        
        # Patrón de validación básico para correos electrónicos
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, value):
            raise ValidationError(
                f"El campo {field_name} debe ser una dirección de correo electrónico válida",
                field=field_name
            )
        
        return value
    
    @staticmethod
    def validate_uuid(value: Any, field_name: str) -> str:
        """
        Valida que un valor sea un UUID válido
        
        Args:
            value: Valor a validar
            field_name: Nombre del campo
            
        Returns:
            UUID validado como cadena
            
        Raises:
            ValidationError: Si el valor no es un UUID válido
        """
        if not isinstance(value, str):
            raise ValidationError(f"El campo {field_name} debe ser una cadena", field=field_name)
        
        value = value.strip()
        
        if not value:
            raise ValidationError(f"El campo {field_name} es obligatorio", field=field_name)
        
        try:
            uuid_obj = uuid.UUID(value)
            return str(uuid_obj)
        except ValueError:
            raise ValidationError(f"El campo {field_name} debe ser un UUID válido", field=field_name)
    
    @staticmethod
    def validate_date(value: Any, field_name: str, format_str: str = "%Y-%m-%d") -> datetime:
        """
        Valida que un valor sea una fecha válida
        
        Args:
            value: Valor a validar
            field_name: Nombre del campo
            format_str: Formato de fecha esperado (por defecto YYYY-MM-DD)
            
        Returns:
            Fecha validada como objeto datetime
            
        Raises:
            ValidationError: Si el valor no es una fecha válida
        """
        if not isinstance(value, str):
            raise ValidationError(f"El campo {field_name} debe ser una cadena", field=field_name)
        
        value = value.strip()
        
        if not value:
            raise ValidationError(f"El campo {field_name} es obligatorio", field=field_name)
        
        try:
            date_obj = datetime.strptime(value, format_str)
            return date_obj
        except ValueError:
            raise ValidationError(
                f"El campo {field_name} debe tener el formato {format_str}",
                field=field_name
            )
    
    @staticmethod
    def validate_url(value: Any, field_name: str) -> str:
        """
        Valida que un valor sea una URL válida
        
        Args:
            value: Valor a validar
            field_name: Nombre del campo
            
        Returns:
            URL validada
            
        Raises:
            ValidationError: Si el valor no es una URL válida
        """
        if not isinstance(value, str):
            raise ValidationError(f"El campo {field_name} debe ser una cadena", field=field_name)
        
        value = value.strip()
        
        if not value:
            raise ValidationError(f"El campo {field_name} es obligatorio", field=field_name)
        
        # Patrón de validación básico para URLs
        pattern = r'^(http|https)://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}[/\w\.-]*$'
        if not re.match(pattern, value):
            raise ValidationError(
                f"El campo {field_name} debe ser una URL válida (http:// o https://)",
                field=field_name
            )
        
        return value
    
    @staticmethod
    def validate_enum(value: Any, field_name: str, valid_values: List[Any]) -> Any:
        """
        Valida que un valor esté dentro de un conjunto de valores válidos
        
        Args:
            value: Valor a validar
            field_name: Nombre del campo
            valid_values: Lista de valores válidos
            
        Returns:
            Valor validado
            
        Raises:
            ValidationError: Si el valor no está en la lista de valores válidos
        """
        if value is None:
            raise ValidationError(f"El campo {field_name} es obligatorio", field=field_name)
        
        if value not in valid_values:
            raise ValidationError(
                f"El campo {field_name} debe ser uno de los siguientes valores: {', '.join(map(str, valid_values))}",
                field=field_name
            )
        
        return value
    
    @staticmethod
    def validate_password(value: Any, field_name: str, min_length: int = 8) -> str:
        """
        Valida que un valor sea una contraseña segura
        
        Args:
            value: Valor a validar
            field_name: Nombre del campo
            min_length: Longitud mínima (por defecto 8)
            
        Returns:
            Contraseña validada
            
        Raises:
            ValidationError: Si el valor no es una contraseña segura
        """
        if not isinstance(value, str):
            raise ValidationError(f"El campo {field_name} debe ser una cadena", field=field_name)
        
        if len(value) < min_length:
            raise ValidationError(
                f"El campo {field_name} debe tener al menos {min_length} caracteres",
                field=field_name
            )
        
        # Verificar complejidad
        has_uppercase = any(c.isupper() for c in value)
        has_lowercase = any(c.islower() for c in value)
        has_digit = any(c.isdigit() for c in value)
        has_special = any(not c.isalnum() for c in value)
        
        if not (has_uppercase and has_lowercase and has_digit):
            raise ValidationError(
                f"El campo {field_name} debe contener al menos una letra mayúscula, una minúscula y un número",
                field=field_name
            )
        
        return value