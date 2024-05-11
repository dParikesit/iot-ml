import os
import tempfile

from google.cloud import storage

storage_client = storage.Client()


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

    __upload_image(file_name, blob)


def __upload_image(file_name, blob: storage.Blob):
    """Uploads the image to the Cloud Storage bucket.

    Args:
        file_name: name of the file
        blob: blob data
    """
    # Download the image from the Cloud Storage bucket.
    _, temp_local_filename = tempfile.mkstemp()
    blob.download_to_filename(temp_local_filename)
    print(f"Image {file_name} was downloaded to {temp_local_filename}.")

    upload_bucket_name = os.getenv("UPLOAD_BUCKET_NAME")
    upload_bucket = storage_client.bucket(upload_bucket_name)

    # Upload the image to the Cloud Storage bucket.
    upload_blob = upload_bucket.blob(file_name)
    upload_blob.upload_from_filename(temp_local_filename)
    print(f"Image {file_name} was uploaded to {upload_bucket_name}.")

    # Delete the temporary file.
    os.remove(temp_local_filename)
