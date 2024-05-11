import datetime
import json

import cv2
from ultralytics import YOLO

from util import read_paddlepaddle, format_license

# load models
yolo_model = YOLO("model/yolov8l.pt")
license_plate_detector = YOLO("model/license_plate_detector.pt")

vehicles = [2, 3, 5, 7]
log_file = open("output/result.log", "w+")


def full_pipeline(image_url: str, log=False, debug=True):
    output = ""
    count = 0
    
    frame = cv2.imread(image_url)

    # detect license plates
    license_plates = license_plate_detector(frame)[0]
    for license_plate in license_plates.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = license_plate

        # crop license plate
        license_plate_crop = frame[int(y1) : int(y2), int(x1) : int(x2), :]

        if debug:
            cv2.imwrite(f"output/{count}.png", license_plate_crop)

        license_plate_text, license_plate_text_score = read_paddlepaddle(license_plate_crop)

        count+=1


        if license_plate_text is not None:
            if log:
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
                    )
                )
            output += format_license(license_plate_text)

    return output

print(full_pipeline("input/4.jpg"))

log_file.close()
