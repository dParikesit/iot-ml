# iot machine learning API

Plate number detection service

## Running Locally

### Setup Environment Variables

There are multiple environment variables that need to be setup in .env files

1. Google Cloud Storage
    - UPLOAD_BUCKET_NAME : bucket name for upload processed image

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

## Deployment To GCP

### Setup GCP

To upload to GCP we need to authenticate

1. Installing SDK https://cloud.google.com/sdk?hl=en
2. Authenticating
    ```
    gcloud auth login
    ```
3. Set Project
    ```
    gcloud config set project {PROJECT_ID}
    ```

### Pushing to Artifact Registry

0. Authenticate artifact registry

    ```
    gcloud auth configure-docker asia-southeast2-docker.pkg.dev

    gcloud artifacts repositories describe {REGISTRY_NAME} --project={PROJECT_ID} --location=asia-southeast2
    ```

1. Tag the image

    ```
    docker tag iot-ml:$TAG asia-southeast2-docker.pkg.dev/parking-system-417615/docker/iot-ml:$TAG
    ```

2. Push to Artifact Registry

    ```
    docker push asia-southeast2-docker.pkg.dev/parking-system-417615/docker/iot-ml:$TAG
    ```
