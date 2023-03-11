import doctest

import boto3


def read_from_s3(bucket_name, aws_file_path):
    """
    Reads files from AWS.

    :param bucket_name: string
    :param aws_file_path: string
    :return: string
    """
    s3 = boto3.client("s3")
    response = s3.get_object(Bucket=bucket_name, Key=aws_file_path)
    file_contents = response["Body"].read().decode("utf-8")
    return file_contents


def list_blobs_in_s3(bucket_name):
    """
    Given a bucket name, returns the blobs in that bucket.

    :param bucket_name: string
    :return: list
    """
    s3 = boto3.client("s3")
    response = s3.list_objects_v2(Bucket=bucket_name)
    blobs = []
    for obj in response["Contents"]:
        blobs.append(obj["Key"])
    return blobs


if __name__ == "__main__":
    doctest.testmod()
