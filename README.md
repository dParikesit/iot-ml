# iot machine learning API

Plate number detection service

## Running Locally

### Building Docker Image

1. Build the image

    ```
    docker build -t iot-ml:$TAG .
    ```

    - **TAG** should be of form **[MAJOR]:[MINOR]**
    - **.** describes the location of the Dockerfile

### Dev: Running Dockerfile locally

1. Run dockerfile:

    ```
    docker run -e PORT=8081 -p 8081:8081 iot-ml:$TAG
    ```

    - -e PORT=8081 sets the app to run on port 8081
    - -p forwards port 8081 from host to 8081 in container
