import doctest

from google.cloud import storage


def upload_to_gcs(bucket_name, local_file_path, gcs_file_name):
    """
    Uploads local files to Google Cloud Storage (GCS).

    :param bucket_name: string
    :param local_file_path: string
    :param gcs_file_name: string
    :return: None
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(gcs_file_name)
    blob.upload_from_filename(local_file_path)


def list_blobs(bucket_name):
    """
    Given a bucket name, returns the blobs in that bucket.

    :param bucket_name: string
    :return: list
    """
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blobs = bucket.list_blobs()
    return list(blobs)


def read_blob_from_gcs(bucket_name, file_name):
    """
    Given a bucket and a file name, returns the file contents as a string.

    :param bucket_name: string
    :param file_name: string
    :return: bytes
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    return blob.download_as_bytes()


def copy_blob(
    bucket_name, blob_name, destination_bucket_name, destination_blob_name,
):
    """
    Copies files from one GCS bucket to another

    :param bucket_name: string
    :param blob_name: string
    :param destination_bucket_name: string
    :param destination_blob_name: string
    :return: None
    """
    storage_client = storage.Client()

    source_bucket = storage_client.bucket(bucket_name)
    source_blob = source_bucket.blob(blob_name)
    destination_bucket = storage_client.bucket(destination_bucket_name)

    blob_copy = source_bucket.copy_blob(
        source_blob,
        destination_bucket,
        destination_blob_name,
        if_generation_match=None,
    )


if __name__ == "__main__":
    doctest.testmod()
