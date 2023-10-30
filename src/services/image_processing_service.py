from fastapi import UploadFile, File
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors
from PIL import Image
from io import BytesIO
import pandas as pd
import json
import numpy as np

class ImageProcessingService:
    
    async def get_defect_details_from_bytes(self, bytes: bytes):
        return await self.__get_defect_details_from_bytes(bytes)
    
    async def generate_report_file_from_bytes(self, bytes: bytes):
        return await self.__generate_report_file_from_bytes(bytes)
    
    async def __get_defect_details_from_bytes(self, bytes: bytes):
        model = YOLO("best.pt")
        result={'detect_objects': None}
        input_image = self.get_image_from_bytes(bytes)
        predictions = model(input_image)
        predict = self.transform_predict_to_df(predictions, model.model.names)
        detect_res = predict[['name', 'confidence']]
        objects = detect_res['name'].values
        
        result['detect_objects_names'] = ', '.join(objects)
        result['detect_objects'] = json.loads(detect_res.to_json(orient='records'))
        return result
    
    async def __generate_report_file_from_bytes(self, bytes: bytes) -> bytes:
        model = YOLO("best.pt")
        input_image = self.get_image_from_bytes(bytes)
        predictions = model(input_image)
        predict = self.transform_predict_to_df(predictions, model.model.names)
        final_image = self.add_bboxs_on_img(image = input_image, predict = predict)
        return self.get_bytes_from_image(final_image)
    
    def get_image_from_bytes(self, binary_image: bytes) -> Image:
        input_image = Image.open(BytesIO(binary_image)).convert("RGB")
        return input_image
    
    def transform_predict_to_df(self, results: list, labeles_dict: dict) -> pd.DataFrame:
        # Transform the Tensor to numpy array
        predict_bbox = pd.DataFrame(results[0].to("cpu").numpy().boxes.xyxy, columns=['xmin', 'ymin', 'xmax','ymax'])
        # Add the confidence of the prediction to the DataFrame
        predict_bbox['confidence'] = results[0].to("cpu").numpy().boxes.conf
        # Add the class of the prediction to the DataFrame
        predict_bbox['class'] = (results[0].to("cpu").numpy().boxes.cls).astype(int)
        # Replace the class number with the class name from the labeles_dict
        predict_bbox['name'] = predict_bbox["class"].replace(labeles_dict)
        return predict_bbox
    
    def add_bboxs_on_img(self, image: Image, predict: pd.DataFrame()) -> Image:
        # Create an annotator object
        annotator = Annotator(np.array(image))

        # sort predict by xmin value
        predict = predict.sort_values(by=['xmin'], ascending=True)

        # iterate over the rows of predict dataframe
        for i, row in predict.iterrows():
            # create the text to be displayed on image
            text = f"{row['name']}: {int(row['confidence']*100)}%"
            # get the bounding box coordinates
            bbox = [row['xmin'], row['ymin'], row['xmax'], row['ymax']]
            # add the bounding box and text on the image
            annotator.box_label(bbox, text, color=colors(row['class'], True))
        # convert the annotated image to PIL image
        return Image.fromarray(annotator.result())
    
    def get_bytes_from_image(self, image: Image) -> bytes:
        return_image = BytesIO()
        image.save(return_image, format='JPEG', quality=85)  # save the image in JPEG format with quality 85
        return_image.seek(0)  # set the pointer to the beginning of the file
        return return_image

    