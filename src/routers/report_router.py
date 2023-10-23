from fastapi import APIRouter
from fastapi import Depends, UploadFile, File
from fastapi.responses import StreamingResponse
from services.image_processing_service import ImageProcessingService

router = APIRouter(
    prefix="/report",
    tags=["Report"]
)

@router.post("/details")
async def generate_report(file: UploadFile = File(...), service = Depends(ImageProcessingService)):
    return await service.get_defect_details(file)

@router.post("/file")
async def generate_report(file: UploadFile = File(...), service = Depends(ImageProcessingService)):
    result_image_bytes = await service.generate_report_file(file)
    return StreamingResponse(result_image_bytes, media_type="image/jpeg")