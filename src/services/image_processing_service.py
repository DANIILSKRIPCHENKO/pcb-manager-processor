from fastapi import UploadFile, File
import torch
from PIL import Image
from io import BytesIO

class ImageProcessingService:
    
    async def get_defect_details(self, file: UploadFile):
        model = torch.hub.load('C:/Users/Danil/Desktop/Git/pcb-manager-fastapi/yolov5', 'custom', path='C:/Users/Danil/Desktop/Git/pcb-manager-fastapi/best.pt', source='local') 
        results = model(Image.open(BytesIO(await file.read())))
        json_results = self.__results_to_json(results.xyxy[0], model)
        return json_results
    
    async def generate_report_file(self, file: UploadFile = File(...)) -> str:
        model = torch.hub.load('C:/Users/Danil/Desktop/Git/pcb-manager-fastapi/yolov5', 'custom', path='C:/Users/Danil/Desktop/Git/pcb-manager-fastapi/best.pt', source='local') 
        results = model(Image.open(BytesIO(await file.read())))
        r_img = results.render()
        image = Image.fromarray(r_img[0])
        image.save("test.jpg")
        return "test.jpg"
    
    def __results_to_json(self, result, model):
        return[
                {
                    "class": int(pred[5]),
                    "class_name": model.model.names[int(pred[5])],
                    "bbox": [int(x) for x in pred[:4].tolist()], #convert bbox results to int from float
                    "confidence": float(pred[4]),
                }
            for pred in result
            ]


    