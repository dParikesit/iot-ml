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

    # Download the image from the Cloud Storage bucket.
    _, temp_local_filename = tempfile.mkstemp()
    blob.download_to_filename(temp_local_filename)

    # temp_local_filename is the file path to the temporary file.
    # Process the image from the temporary file.

    # with open(temp_local_filename, "rb") as image_file:
    #     image = image_file.read()

    # Save the image to a new file

    # with open(temp_local_filename, "wb") as image_file:
    #     image_file.write(image)

    # Upload the processed image to the Cloud Storage bucket.
    __upload_image(file_name, temp_local_filename)


def __upload_image(blob_name, file_name):
    """Uploads the image to the Cloud Storage bucket.

    Args:
        blob_name: name of the blob in the bucket
        file_name: name of the file in local storage (tempfile)
    """

    upload_bucket_name = os.getenv("UPLOAD_BUCKET_NAME")
    upload_bucket = storage_client.bucket(upload_bucket_name)

    # Upload the image to the Cloud Storage bucket.
    upload_blob = upload_bucket.blob(blob_name)
    upload_blob.upload_from_filename(file_name)
    print(f"Image {blob_name} was uploaded to {upload_bucket_name}.")

    # Delete the temporary file.
    os.remove(file_name)
