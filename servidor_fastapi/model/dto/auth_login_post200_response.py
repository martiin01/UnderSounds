# coding: utf-8

"""
    Music E-Commerce API - Respuesta de Login Exitoso
"""  # noqa: E501

from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictStr
# --- Importa el DTO UserProfile ---
from model.dto.user_profile import UserProfile # Asegúrate que esta ruta de importación sea correcta
from typing import Any, ClassVar, Dict, List, Optional
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class AuthLoginPost200Response(BaseModel):
    """
    Respuesta exitosa para el login, contiene el token JWT y el perfil del usuario.
    """ # noqa: E501
    token: StrictStr = Field(..., description="Token JWT para la sesión")
    # --- Campo user añadido ---
    user: UserProfile = Field(..., description="Perfil del usuario logueado")

    # --- Metadatos y Configuración (Pydantic v2) ---
    __properties: ClassVar[list[str]] = ["token", "user"]

    model_config = ConfigDict(
        populate_by_name=True,      # Permite usar alias si UserProfile los tuviera
        validate_assignment=True,   # Valida al asignar valores a campos
        protected_namespaces=(),    # Necesario para Pydantic v2
        # extra='ignore'            # Opcional: Ignorar campos extra no definidos
    )

    # --- Métodos de Conversión (Usando Pydantic v2) ---

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        # Usa model_dump para obtener un dict, incluyendo el user anidado
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model"""
        # model_dump_json maneja la serialización de modelos anidados
        return self.model_dump_json(by_alias=True) # exclude_unset=True es opcional

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of AuthLoginPost200Response from a JSON string"""
        # model_validate_json maneja la deserialización de modelos anidados
        return cls.model_validate_json(json_str)

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model."""
        # model_dump maneja la conversión a dict de modelos anidados
        return self.model_dump(by_alias=True) # exclude_unset=True es opcional

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of AuthLoginPost200Response from a dict"""
        if obj is None:
            raise ValueError("Cannot create AuthLoginPost200Response from None")

        if not isinstance(obj, dict):
             try:
                 # Intenta validar directamente si no es un dict
                 return cls.model_validate(obj)
             except Exception as e:
                 raise TypeError(f"Input must be a dictionary or a valid model instance, got {type(obj)}") from e

        # Pydantic v2 puede validar directamente el diccionario si las claves coinciden
        # y maneja la validación del 'user' anidado si es un diccionario también.
        try:
            # Asegurarse de que los campos requeridos estén presentes
            required_fields = {"token", "user"}
            missing_fields = required_fields - obj.keys()
            if missing_fields:
                # Podrías ser más específico si 'user' falta o si 'token' falta
                raise ValueError(f"Faltan campos obligatorios en el diccionario: {missing_fields}")

            # Validar el diccionario completo, Pydantic se encargará de validar 'user' con UserProfile
            _obj = cls.model_validate(obj)
        except Exception as e:
            # Proporcionar más contexto en caso de error de validación
            print(f"Error validating AuthLoginPost200Response data from dict: {obj}")
            raise e

        return _obj
