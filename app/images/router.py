from fastapi import APIRouter, UploadFile
import shutil

from config import settings

router = APIRouter(
    prefix="/images",
    tags=["Загрузка картинок"]
)

@router.post("/hotels")
async def add_hotel_image(name: int, file: UploadFile):
    with open(f"{settings.STATIC_IMAGES_PATH}/{name}.webp", "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)