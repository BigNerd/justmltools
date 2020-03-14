import boto3

from typing import Optional
from justmltools.s3.aws_credentials import AwsCredentials


class S3BucketObjectUploader:

    def __init__(self, credentials: Optional[AwsCredentials] = None):
        if credentials is None:
            self.__s3 = boto3.resource("s3")
        else:
            self.__s3 = boto3.resource(
                's3',
                aws_access_key_id=credentials.aws_secret_access_key_id,
                aws_secret_access_key=credentials.aws_secret_access_key,
                region_name=credentials.region_name
            )

    def upload(self, source_path_and_name: str, bucket: str, key: str):
        """
        Uploads file from target path and name as object to S3 bucket using key

        :param source_path_and_name: File system path to upload file from
        :param bucket: Name of the S3 bucket
        :param key: Key of the S3 object to upload to
        """

        self.__s3.Bucket(bucket).upload_file(source_path_and_name, bucket, key)
