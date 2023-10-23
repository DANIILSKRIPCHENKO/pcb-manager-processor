from fastapi import FastAPI, Depends
from services.image_processing_service import ImageProcessingService
from routers import report_router
import uvicorn

app = FastAPI(title="Pcb Manager")

app.include_router(report_router.router)

# For debugging in vs code
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)