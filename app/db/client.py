from dataclasses import dataclass
from typing import Any
import os

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection


@dataclass
class MongoDBClient:
    client: AsyncIOMotorClient
    db: AsyncIOMotorDatabase
    song_collection: AsyncIOMotorCollection

    def __init__(self) -> None:
        mongodb_url: str = os.environ["MONGODB_URL"]
        self.client = AsyncIOMotorClient(mongodb_url)
        self.db = self.client["yousician"]
        self.song_collection = self.db.get_collection("songs")
