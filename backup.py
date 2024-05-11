import datetime
import json

import cv2
from ultralytics import YOLO

from util import get_car, read_paddlepaddle, format_license

# load models
yolo_model = YOLO("model/yolov8n.pt")
license_plate_detector = YOLO("model/license_plate_detector.pt")

vehicles = [2, 3, 5, 7]
log_file = open("output/result.log", "w+")


def full_pipeline(image_url: str, log=True, debug=False):
    frame = cv2.imread(image_url)

    # detect vehicles
    detections = yolo_model(frame)[0]
    detections_ = []
    for detection in detections.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = detection
        if int(class_id) in vehicles:
            detections_.append([x1, y1, x2, y2, score])

    # detect license plates
    license_plates = license_plate_detector(frame)[0]
    for license_plate in license_plates.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = license_plate

        # assign license plate to car
        xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, detections_)

        if car_id != -1:
            # crop license plate
            license_plate_crop = frame[int(y1) : int(y2), int(x1) : int(x2), :]

            if debug:
                cv2.imwrite(f"output/{image_url}", license_plate_crop)

            # process license plate
            license_plate_crop_gray = cv2.cvtColor(
                license_plate_crop, cv2.COLOR_BGR2GRAY
            )
            _, license_plate_crop_thresh = cv2.threshold(
                license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV
            )

            # read license plate number
            license_plate_text, license_plate_text_score = read_paddlepaddle(
                f"output/{count}.png"
            )

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
            print(f"license text {format_license(license_plate_text)}")
            return format_license(license_plate_text)
        else:
            return None


print(full_pipeline("input/4.jpg"))

log_file.close()
