import boto3

from typing import Optional
from justmltools.s3.aws_credentials import AwsCredentials
from justmltools.s3.s3_bucket_object_finder import S3BucketObjectFinder


class S3Copier:

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
        self.__s3_object_finder = S3BucketObjectFinder(credentials=credentials)

    def copy_s3_objects(self, bucket, from_prefix="", from_suffix="", to_prefix=""):
        """
        Copies objects whose keys match from_prefix and from_suffix to the same bucket
        using to_prefix instead of from_prefix.

        :param bucket: Name of the S3 bucket.
        :param from_prefix: Only copy objects whose keys start with
            this prefix (optional).
        :param from_suffix: Only copy objects whose keys end with
            this suffix (optional).
        :param to_prefix: Replace from_prefix with to_prefix to create the copy target key
        :return generates pairs of source key and target key which have been copied
        """
        target_bucket = self.__s3.Bucket(bucket)
        for source_key in self.__s3_object_finder.get_matching_s3_keys(
                bucket=bucket, prefix=from_prefix, suffix=from_suffix):
            source_ref = {'Bucket': bucket, 'Key': source_key}
            target_key: str = source_key.replace(from_prefix, to_prefix)
            target_bucket.copy(CopySource=source_ref, Key=target_key)
            yield source_key, target_key
