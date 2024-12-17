from fastapi import APIRouter


router = APIRouter()


@router.get("/")
def get_songs():
    return {"message": "List of songs"}


@router.post("/rating")
def get_songs():
    return {"message": "List of songs"}


@router.get("/search")
def search_song():
    return {"message": "List of songs"}


@router.get("/avg/difficulty")
def get_average_level():
    return {"message": "Average difficulty"}


@router.get("/avg/rating/<song_id>")
def get_songs(song_id):
    return {"message": "List of songs"}
