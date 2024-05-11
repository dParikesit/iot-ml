import datetime
import json

import cv2
from ultralytics import YOLO

from util import get_car, read_paddlepaddle, format_license, conv_class
from typing import Tuple, List

# load models
yolo_model = YOLO("model/yolov8l.pt")
license_plate_detector = YOLO("model/license_plate_detector.pt")

vehicles = [2, 3, 5, 7]


def full_pipeline(image_url: str, log=False, debug=False) -> List[Tuple[str, str]]:
    """
    Full pipeline to process an image

    Args:
        image_url (str): path to the image
        log (bool): whether to log the results
        debug (bool): debug flag

    Returns:
        List[Tuple[str, str]]: list of tuples of vehicle type and license plate
    """
    output = []
    count = 0

    frame = cv2.imread(image_url)

    # detect vehicles
    detections = yolo_model(frame)[0]
    detections_ = []
    for detection in detections.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = detection
        if int(class_id) in vehicles:
            detections_.append([x1, y1, x2, y2, score, class_id])

    # detect license plates
    license_plates = license_plate_detector(frame)[0]
    for license_plate in license_plates.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = license_plate

        # assign license plate to car
        xcar1, ycar1, xcar2, ycar2, score, class_id = get_car(
            license_plate, detections_
        )

        if class_id != -1:
            # crop license plate
            license_plate_crop = frame[int(y1) : int(y2), int(x1) : int(x2), :]

            if debug:
                cv2.imwrite(f"output/{image_url}", license_plate_crop)

            # read license plate number
            license_plate_text, license_plate_text_score = read_paddlepaddle(
                license_plate_crop
            )

            count += 1

            if license_plate_text is not None:
                if log:
                    log_file = open("output/result.log", "a")

                    log_file.write(
                        json.dumps(
                            {
                                "license_plate": {
                                    "bbox": [x1, y1, x2, y2],
                                    "vehicle": conv_class(class_id, yolo_model.names),
                                    "text": license_plate_text,
                                    "bbox_score": score,
                                    "text_score": license_plate_text_score,
                                },
                                "timestamp": datetime.datetime.now().strftime(
                                    "%d/%m/%Y, %H:%M:%S"
                                ),
                            }
                        )
                        + "\n"
                    )

                    log_file.close()
                output.append(
                    (
                        conv_class(class_id, yolo_model.names),
                        format_license(license_plate_text),
                    )
                )
    return output
