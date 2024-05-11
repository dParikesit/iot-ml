import os
import tempfile

from google.cloud import storage

import full as full_process
import requests

storage_client = storage.Client()
BACKEND_URL = os.getenv("BACKEND_URL")


def process_image(data):
    """Blurs uploaded images that are flagged as Adult or Violence.

    Args:
        data: Pub/Sub message data
    """
    file_data = data

    file_name = file_data["name"]
    bucket_name = file_data["bucket"]

    blob = storage_client.bucket(bucket_name).get_blob(file_name)

    print(f"Analyzing {file_name}.")

    # Download the image from the Cloud Storage bucket.
    _, temp_local_filename = tempfile.mkstemp()
    blob.download_to_filename(temp_local_filename)

    detected = full_process.full_pipeline(temp_local_filename)

    if detected:
        vehicle_type, plate_number = detected[0]
        print(f"Vehicle type: {vehicle_type}, Plate number: {plate_number}")

    vehicle_type, plate_number = full_process.full_pipeline(temp_local_filename)[0]

    # Send the image to the backend.
    requests.post(
        BACKEND_URL + "/vehicle/action/",
        json={
            "plate_number": plate_number,
            "image_url": f"https://storage.googleapis.com/{bucket_name}/{file_name}",
        },
    )

    print(f"Vehicle type: {vehicle_type}, Plate number: {plate_number}")
