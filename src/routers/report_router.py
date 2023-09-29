from fastapi import APIRouter
from fastapi import Depends, UploadFile, File
from fastapi.responses import FileResponse
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
    report_file_path = await service.generate_report_file(file)
    return FileResponse(report_file_path)