import boto3
import errno
import os
import pathlib

from typing import Optional
from justmltools.s3.aws_credentials import AwsCredentials


class S3BucketObjectDownloader:

    def __init__(self, credentials: Optional[AwsCredentials] = None):
        if credentials is None:
            self.__s3 = boto3.resource("s3")
        else:
            self.__s3 = boto3.resource(
                "s3",
                aws_access_key_id=credentials.aws_secret_access_key_id,
                aws_secret_access_key=credentials.aws_secret_access_key,
                region_name=credentials.region_name
            )

    def download(self, bucket: str, key: str, target_path_and_name: str, override_existing_file=False):
        """
        Downloads object from S3 bucket as file with target path and name

        :param bucket: Name of the S3 bucket
        :param key: Key of the S3 object to download
        :param target_path_and_name: File system path to download object as file to
        :param override_existing_file: whether to override any already existing file
            with same path and name as target path and name (optional)
        """
        if not override_existing_file:
            if os.path.isfile(target_path_and_name):
                raise FileExistsError(errno.EEXIST, os.strerror(errno.EEXIST), target_path_and_name)

        if not key.endswith('/'):  # object is file, not a 'folder' object
            pathlib.Path(target_path_and_name).parent.mkdir(parents=True, exist_ok=True)
            self.__s3.Bucket(bucket).download_file(key, target_path_and_name)
        else:  # object is a 'folder'
            if not os.path.isdir(target_path_and_name):
                pathlib.Path(target_path_and_name).mkdir(parents=True, exist_ok=True)

    def get(self, bucket: str, key: str):
        """
        Gets object body from s3 bucket

        :param bucket: Name of the S3 bucket
        :param key: Key of the S3 object to download
        :return: botocore.response.StreamingBody
        """
        body = self.__s3.Object(bucket, key).get()["Body"]
        return body
