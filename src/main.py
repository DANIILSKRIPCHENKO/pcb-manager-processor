from fastapi import FastAPI, Depends
from services.image_processing_service import ImageProcessingService
from routers import report_router

app = FastAPI(title="Pcb Manager")

app.include_router(report_router.router)