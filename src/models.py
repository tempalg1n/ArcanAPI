from typing import Optional, List

from pydantic import BaseModel


class DescriptionsSchema(BaseModel):
    general: str
    personal_condition: Optional[str] = None
    deep_level: Optional[str] = None
    job: Optional[str] = None
    finances: Optional[str] = None
    personal_relations: Optional[str] = None
    health: Optional[str] = None
    upside_down: Optional[str] = None
    combinations: Optional[str] = None
    archetypal: Optional[str] = None
    remarks: Optional[str] = None


class ArcaneSchema(BaseModel):
    name: str
    attrs: List[str]
    card: str
    categories: DescriptionsSchema

    class Config:
        schema_extra = {
            "example": {
                "name": "Шут",
                "attrs": "Набор$атрибутов",
                "card": "https://taro.lv/images/uploads/167x300/18-arc-00.jpg",
                "categories": {
                    "general": "Общее описание",
                    "personal_condition": "Личностное состояние",
                    "deep_level": "На глубоком уровне",
                    "job": "Карьера",
                    "finances": "Финансы",
                    "personal_relations": "Личные отношения",
                    "health": "Здоровье",
                    "upside_down": "Перевернутая карта",
                    "combinations": "В комбинации с другими картами",
                    "archetypal": "Архетипы",
                    "remarks": "Примечания"
                }
            }
        }


class UserSchema(BaseModel):
    tg_id: int
    first_name: str
    username: Optional[str] = None
    data: Optional[dict] = None

    class Config:
        schema_extra = {
            "example": {
                "tg_id": "11112222",
                "first_name": "Ivan",
                "username": None,
                "data": None,
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
