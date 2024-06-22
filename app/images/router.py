from fastapi import APIRouter, UploadFile
import shutil

from app.tasks.tasks import process_pic
from app.config import settings

router = APIRouter(
    prefix="/images",
    tags=["Загрузка картинок"]
)

@router.post("/hotels")
async def add_hotel_image(name: int, file: UploadFile):
    im_path = settings.STATIC_IMAGES_PATH + f"/{name}.webp"
    with open(im_path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    process_pic.delay(im_path)