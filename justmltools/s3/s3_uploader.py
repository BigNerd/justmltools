from typing import List, Optional

from justmltools.s3.aws_credentials import AwsCredentials
from justmltools.s3.s3_bucket_object_uploader import S3BucketObjectUploader


class S3Uploader:

    def __init__(self, credentials: Optional[AwsCredentials] = None):
        self.__credentials = credentials

    def upload(self,
               source_file_paths: List[str],
               bucket: str,
               removable_source_path_prefix: str = "",
               prependable_key_prefix: str = ""):
        """
        Uploads all source file paths to an S3 bucket.
        Maps from source file paths to keys by removing source path prefix and prepending key prefix

        :param bucket: name of the S3 bucket
        :param source_file_paths: absolute file system paths of files to upload
        :param removable_source_path_prefix:
                prefix to remove from each source file path for key mapping
        :param prependable_key_prefix:
                prefix to prepend to each source file path (after removal of source path prefix) for key mapping
        """
        s3_bucket_object_uploader: S3BucketObjectUploader = S3BucketObjectUploader(credentials=self.__credentials)
        for source_file_path in source_file_paths:
            key = source_file_path
            if removable_source_path_prefix and key.startswith(removable_source_path_prefix):
                key = key[len(removable_source_path_prefix):]  # removes removable_source_path_prefix
            if prependable_key_prefix:
                key = prependable_key_prefix + key
            s3_bucket_object_uploader.upload(
                source_path_and_name=source_file_path, bucket=bucket, key=key)
