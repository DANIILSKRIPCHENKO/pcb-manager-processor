from fastapi import APIRouter
from typing import Annotated
from fastapi import Depends, UploadFile, File, Request
from fastapi.responses import StreamingResponse
from services.image_processing_service import ImageProcessingService

router = APIRouter(
    prefix="/report",
    tags=["Report"]
)

@router.post("/details/from-file")
async def generate_report(file: bytes = File(...), service = Depends(ImageProcessingService)):
    return await service.get_defect_details_from_bytes(file)

@router.post("/file/from-file")
async def generate_report(file: bytes = File(...), service = Depends(ImageProcessingService)):
    result_image_bytes = await service.generate_report_file_from_bytes(file)
    return StreamingResponse(result_image_bytes, media_type="image/jpeg")
