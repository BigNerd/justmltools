import boto3

from typing import Optional
from justmltools.s3.aws_credentials import AwsCredentials

# Based on code from https://alexwlchan.net/2019/07/listing-s3-keys/
# Copyright © 2012–19 Alex Chan. Released under MIT license.


class S3BucketObjectFinder:

    def __init__(self, credentials: Optional[AwsCredentials] = None):
        if credentials is None:
            self.__s3 = boto3.client("s3")
        else:
            self.__s3 = boto3.client(
                "s3",
                aws_access_key_id=credentials.aws_secret_access_key_id,
                aws_secret_access_key=credentials.aws_secret_access_key,
                region_name=credentials.region_name
            )

    def get_matching_s3_objects(self, bucket, prefix="", suffix=""):
        """
        Generate objects in an S3 bucket.

        :param bucket: Name of the S3 bucket.
        :param prefix: Only fetch objects whose keys start with
            this prefix (optional).
        :param suffix: Only fetch objects whose keys end with
            this suffix (optional).
        """
        paginator = self.__s3.get_paginator("list_objects_v2")

        kwargs = {'Bucket': bucket}

        # We can pass the prefix directly to the S3 API.  If the user has passed
        # a tuple or list of prefixes, we go through them one by one.
        if isinstance(prefix, str):
            prefixes = (prefix, )
        else:
            prefixes = prefix

        for key_prefix in prefixes:
            kwargs["Prefix"] = key_prefix

            for page in paginator.paginate(**kwargs):
                try:
                    contents = page["Contents"]
                except KeyError:
                    return

                for obj in contents:
                    key = obj["Key"]
                    if key.endswith(suffix):
                        yield obj

    def get_matching_s3_keys(self, bucket, prefix="", suffix=""):
        """
        Generate the keys in an S3 bucket.

        :param bucket: Name of the S3 bucket.
        :param prefix: Only fetch keys that start with this prefix (optional).
        :param suffix: Only fetch keys that end with this suffix (optional).
        """
        for obj in self.get_matching_s3_objects(bucket, prefix, suffix):
            yield obj["Key"]
