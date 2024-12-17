from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from bson import ObjectId


class Song(BaseModel):
    id: Optional[ObjectId] = Field(alias="_id", default=None)
    title: str = Field(...)
    artist: str = Field(...)
    difficulty: float = Field(...)
    level: int = Field(...)
    released: str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "title": "Wishing In The Night",
                "artist": "The Yousicians",
                "difficulty": 10.98,
                "level": 9,
                "released": "2016-01-01",
            }
        },
    )
