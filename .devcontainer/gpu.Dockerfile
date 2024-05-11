# FROM nvcr.io/nvidia/paddlepaddle:24.03-py3
FROM nvcr.io/nvidia/paddlepaddle:24.03-py3
RUN pip install wheel
RUN pip install --upgrade tensorrt onnx onnxsim onnxruntime-gpu

ARG YOLO_MAJOR_VERSION=8
ARG YOLO_VERSION=8.2.0
ARG YOLO_SIZE=l

ADD https://github.com/ultralytics/assets/releases/download/v0.0.0/Arial.ttf \
    https://github.com/ultralytics/assets/releases/download/v0.0.0/Arial.Unicode.ttf \
    /root/.config/Ultralytics/

# Install linux packages
# g++ required to build 'tflite_support' and 'lap' packages, libusb-1.0-0 required for 'tflite_support' package
RUN apt update \
    && apt install --no-install-recommends -y gcc git zip curl htop libgl1 libglib2.0-0 libpython3-dev gnupg g++ libusb-1.0-0

# Security updates
# https://security.snyk.io/vuln/SNYK-UBUNTU1804-OPENSSL-3314796
RUN apt upgrade --no-install-recommends -y openssl tar

WORKDIR /workspace/docker/yolo
RUN pip install ultralytics==${YOLO_VERSION} --ignore-installed 
ADD https://github.com/ultralytics/assets/releases/download/v${YOLO_VERSION}/yolov${YOLO_MAJOR_VERSION}${YOLO_SIZE}.pt .
ADD https://github.com/Muhammad-Zeerak-Khan/Automatic-License-Plate-Recognition-using-YOLOv8/raw/main/license_plate_detector.pt .

# export tensorrt format. yolov8l.engine
# RUN yolo export model=yolov${YOLO_MAJOR_VERSION}${YOLO_SIZE}.pt format=engine
# RUN yolo export model=license_plate_detector.pt format=engine

RUN pip install ipykernel paddleocr

# WORKDIR /workspace/docker/paddlepaddle

# RUN git clone https://github.com/PaddlePaddle/PaddleOCR.git
# RUN wget https://paddleocr.bj.bcebos.com/PP-OCRv4/english/en_PP-OCRv4_rec_infer.tar
# RUN tar xf en_PP-OCRv4_rec_infer.tar
# RUN rm en_PP-OCRv4_rec_infer.tar

# python3 tools/infer/predict_rec.py --image_dir="./doc/imgs_words/en/word_1.png" --rec_model_dir="./en_PP-OCRv4_rec_infer/" --rec_char_dict_path="ppocr/utils/en_dict.txt"
# python3 tools/infer/predict_det.py --image_dir="./doc/imgs/1.jpg" --det_model_dir="./ch_PP-OCRv3_det_infer/" --use_tensorrt=True

# Set environment variables
ENV OMP_NUM_THREADS=1
# Avoid DDP error "MKL_THREADING_LAYER=INTEL is incompatible with libgomp.so.1 library" https://github.com/pytorch/pytorch/issues/37377
ENV MKL_THREADING_LAYER=GNU

ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility