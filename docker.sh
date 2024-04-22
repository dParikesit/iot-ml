#! /bin/bash

# Mount a local directory into the container
docker run -t --name iot --ipc=host --gpus all -v .:/app/iot ultralytics/ultralytics:latest