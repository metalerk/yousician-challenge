from fastapi import FastAPI
from app.api.v1.routes import song


app = FastAPI(title="Yousician API", version="1.0.0")

# include routes
app.include_router(song.router, prefix="/songs", tags=["Songs"])
app.include_router(song.router, prefix="/songs", tags=["Songs"])
app.include_router(song.router, prefix="/songs", tags=["Songs"])
app.include_router(song.router, prefix="/songs", tags=["Songs"])
app.include_router(song.router, prefix="/songs", tags=["Songs"])
