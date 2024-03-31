import os
from typing import BinaryIO

import boto3


class UploadService:
    """Service for upload-related tasks."""

    @staticmethod
    def upload_file_to_aws(file: BinaryIO, filename: str, container: str):
        """Create a function for the file upload endpoint."""
        s3 = boto3.resource(
            service_name="s3",
            region_name=os.getenv("AWS_DEFAULT_REGION"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

        s3.Bucket(os.getenv(container)).put_object(Key=filename, Body=file)

    @staticmethod
    def delete_file_from_aws(filename: str, container: str):
        """Create a function for the file deletion endpoint."""
        s3 = boto3.resource(
            service_name="s3",
            region_name=os.getenv("AWS_DEFAULT_REGION"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

        bucket = s3.Bucket(os.getenv(container))
        full_filenames = list(bucket.objects.filter(Prefix=filename))
        full_filename = full_filenames[0].key
        s3.Object(os.getenv(container), full_filename).delete()