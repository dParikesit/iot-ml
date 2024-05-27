import datetime
import json

import cv2
from ultralytics import YOLO

from util import read_paddlepaddle, format_license

# load models
yolo_model = YOLO("model/yolov8l.pt")
license_plate_detector = YOLO("model/license_plate_detector.pt")

vehicles = [2, 3, 5, 7]

def full_pipeline(image_url: str, log=False, debug=True, file_name: str=""):
    output = []
    count = 0

    try:
        frame = cv2.imread(image_url)
        if frame is None:
            raise Exception("cv2 error")

        # detect license plates
        license_plates = license_plate_detector(frame)[0]

        if(len(license_plates)==0):
            raise Exception("plate error")
        
        for license_plate in license_plates.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = license_plate

            # crop license plate
            license_plate_crop = frame[int(y1) : int(y2), int(x1) : int(x2), :]

            if debug:
                cv2.imwrite(f"output/{file_name}", license_plate_crop)

            license_plate_text, license_plate_text_score = read_paddlepaddle(license_plate_crop)

            count+=1

            if license_plate_text is not None:
                if log:
                    log_file = open("output/result.log", "a")

                    log_file.write(
                        json.dumps(
                            {
                                "license_plate": {
                                    "bbox": [x1, y1, x2, y2],
                                    "text": license_plate_text,
                                    "bbox_score": score,
                                    "text_score": license_plate_text_score,
                                },
                                "timestamp": datetime.datetime.now().strftime(
                                    "%d/%m/%Y, %H:%M:%S"
                                ),
                            }
                        ) + "\n"
                    )

                    log_file.close()
                output.append(format_license(license_plate_text))
        return output
    except Exception as e:
        print("Error")
        raise e

# print(full_pipeline("input/4.jpg"))
