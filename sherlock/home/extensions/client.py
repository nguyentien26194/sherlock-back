from datetime import timedelta
from pathlib import PurePosixPath
from typing import Dict, Optional

import boto3
import botocore
from botocore.client import Config
from django.apps import apps

S3_RESSOURCE_NAME = "s3"
MIN_SIZE = 1
MAX_SIZE = 100 * 1024 * 1024
POST_CONDITIONS = [
    {"acl": "private"},
    ["content-length-range", MIN_SIZE, MAX_SIZE],
    {"success_action_status": "201"},
]
UPLOAD_FIELDS = {
    "acl": "private",
    "success_action_status": "201",
}


class S3Client:
    def __init__(
        self, bucket_name: Optional[str] = None, aws_region: Optional[str] = None
    ) -> None:
        # Credentials are fetched from environement variables
        self.client = boto3.client(
            S3_RESSOURCE_NAME,
            region_name=aws_region or apps.get_app_config("home").AWS_REGION,
            config=Config(signature_version="s3v4"),
        )
        self.bucket_name = bucket_name or apps.get_app_config("home").S3_BUCKET_NAME

    def check_if_file_exists(self, filepath: PurePosixPath):
        try:
            key = S3Client.posix_path_to_key(filepath)
            self.client.get_object(Bucket=self.bucket_name, Key=key)
        except botocore.exceptions.ClientError as e:
            return False
        return True

    def delete_existed_file(self, filepath: PurePosixPath):
        key = S3Client.posix_path_to_key(filepath)
        return self.client.delete_object(Bucket=self.bucket_name, Key=key)

    def generate_upload_presigned_url(
        self, filepath: PurePosixPath, expiry: timedelta
    ) -> Dict:
        key = S3Client.posix_path_to_key(filepath)
        return self.client.generate_presigned_post(
            Bucket=self.bucket_name,
            Key=key,
            Fields={**UPLOAD_FIELDS, "bucket": self.bucket_name},
            Conditions=POST_CONDITIONS + [{"key": key}, {"bucket": self.bucket_name}],
            ExpiresIn=int(expiry.total_seconds()),
        )

    @staticmethod
    def posix_path_to_key(path: PurePosixPath):
        """Helper to compute S3 key from PurePosixPath

        If the key is absolute ie "/myfile.txt" S3 creates a folder with a blank name at the
        root of the bucket. To avoid such behavior the path is taken relatively to its root.
        This is similar to restricting filepaths to be **relative** PurePosixPaths.
        PurePosixPath("/test.jpg").relative_to(PurePosixPath("/test.jpg").root) -> PurePosixPath('test.jpg')
        PurePosixPath("test.jpg").relative_to(PurePosixPath("test.jpg").root) -> PurePosixPath('test.jpg')
        """
        return str(path.relative_to(path.root))
