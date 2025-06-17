# coding: utf-8

"""
    Music E-Commerce API - Product DTO
    Alineado con schema.sql
"""  # noqa: E501

from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional, Union
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class Product(BaseModel):
    """
    DTO para Productos, con nombres de campo iguales a schema.sql
    """ # noqa: E501
    # --- Campos exactamente como en schema.sql ---
    id: Optional[StrictStr] = Field(default=None, description="Identificador único del producto (PK)")
    nombre: StrictStr = Field(..., description="Nombre del producto")
    imagen: StrictStr = Field(..., description="URL/path de la imagen del producto")
    precio: Union[StrictFloat, StrictInt] = Field(..., description="Precio del producto")
    fecha: StrictStr = Field(..., description="Fecha asociada al producto (YYYY-MM-DD)")
    tipo: StrictStr = Field(..., description="Categoría del producto (vinilos, cds, cassettes, camisetas)")
    estilo: StrictStr = Field(..., description="Estilo/descripción del producto")
    autor: StrictStr = Field(..., description="ID del usuario artista que subió el producto (FK)")

    # --- Metadatos y Configuración ---
    # Lista de propiedades con los nombres exactos del schema
    __properties: ClassVar[list[str]] = ["id", "nombre", "imagen", "precio", "fecha", "tipo", "estilo", "autor"]

    @field_validator('tipo')
    def tipo_validate_enum_and_normalize(cls, value):
        """Valida que el tipo sea uno de los permitidos y normaliza 'd.compactos'."""
        if value is None:
             # Aunque el campo es obligatorio, Pydantic puede pasar None temporalmente
             raise ValueError("El campo 'tipo' no puede ser nulo")

        value_lower = value.lower()
        if value_lower in ('D.Compactos', 'disco', 'compacto', 'disco compacto','d.compacto', 'd.compactos', 'compacto disco', 'compacto disco compacto'):
            # Normalizar a 'cds'
            value_lower = 'cds'
        allowed_types = ('vinilos', 'cds', 'cassettes', 'camisetas', 'digital')

        # Normalizar 'd.compactos' y similares a 'cds'
        

        if value_lower not in allowed_types:
            raise ValueError(f"El tipo debe ser uno de {allowed_types}, se recibió '{value}'")

        # Devolver el valor normalizado en minúsculas
        return value_lower

    model_config = ConfigDict(
        # populate_by_name=True, # Ya no es necesario al no usar alias
        validate_assignment=True, # Valida al asignar valores a campos
        protected_namespaces=(), # Necesario para Pydantic v2
        extra='ignore' # Ignorar campos extra si vienen de algún sitio
    )

    # --- Métodos de Conversión (Usando Pydantic v2) ---

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.model_dump())

    def to_json(self) -> str:
        """Returns the JSON representation of the model"""
        return self.model_dump_json(exclude_unset=True) # exclude_unset=True es opcional

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of Product from a JSON string"""
        return cls.model_validate_json(json_str)

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model."""
        return self.model_dump(exclude_unset=True) # exclude_unset=True es opcional

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of Product from a dict"""
        if obj is None:
            raise ValueError("Cannot create Product from None")

        if not isinstance(obj, dict):
             try:
                 # Intenta validar directamente si no es un dict
                 return cls.model_validate(obj)
             except Exception as e:
                 raise TypeError(f"Input must be a dictionary or a valid model instance, got {type(obj)}") from e

        # Pydantic v2 maneja el mapeo directamente si los nombres coinciden
        try:
            # Asegurarse de que los campos obligatorios estén presentes
            required_fields = {"nombre", "imagen", "precio", "fecha", "tipo", "estilo", "autor"}
            missing_fields = required_fields - obj.keys()
            if missing_fields:
                raise ValueError(f"Faltan campos obligatorios en el diccionario: {missing_fields}")

            # Crear instancia validando los datos
            _obj = cls.model_validate(obj)
        except Exception as e:
            print(f"Error validating Product data from dict: {obj}")
            raise e

        return _obj
