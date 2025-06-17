from typing import Optional, Dict, Any, TypeVar
from pydantic import BaseModel, Field
import json
import pprint

SelfForum = TypeVar('SelfForum', bound='Forum')

class Forum(BaseModel):
    id: Optional[int] = Field(None, description="ID del post del foro")
    idUser: int = Field(..., description="ID del usuario que opina")
    idProducto: int = Field(..., description="ID del producto que se va a opinar")
    critica: str = Field(..., description="Texto de la crítica")

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SelfForum:
        """Create an instance of Forum from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.
        
        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:
         * `None` is only added to the output dict for nullable fields that
           were set at model initialization. Other fields with value `None`
           are ignored.
        """
        _dict = self.model_dump(
            by_alias=True,
            exclude={},
            exclude_none=True,
        )
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> SelfForum:
        """Create an instance of Forum from a dict"""
        if obj is None:
            return None
        if not isinstance(obj, dict):
            return cls.model_validate(obj)
        _obj = cls.model_validate({
            "id": obj.get("id"),
            "idUser": obj.get("idUser"),
            "idProducto": obj.get("idProducto"),
            "critica": obj.get("critica")
        })
        return _obj

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "idUser": 2,
                "idProducto": 5,
                "critica": "Excelente producto, muy recomendable."
            }
        }