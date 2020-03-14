import os

from typing import Optional

from justmltools.s3.aws_credentials import AwsCredentials
from justmltools.s3.s3_bucket_object_downloader import S3BucketObjectDownloader
from justmltools.s3.s3_bucket_object_finder import S3BucketObjectFinder


class S3Downloader:

    def __init__(self, credentials: Optional[AwsCredentials] = None):
        self.__credentials = credentials

    def download(self, bucket, target_path,
                 override_existing_files=False, key_prefix='', key_suffix='', prune_key_prefix=True):
        """
        Downloads all objects from an S3 bucket whose keys match both prefix and suffix to the given target path.

        :param bucket: Name of the S3 bucket
        :param target_path: File system path to download files to
        :param override_existing_files: Whether to override any existing file (optional, default False)
        :param key_prefix: Only fetch objects whose keys start with this prefix (optional, default '')
        :param key_suffix: Only fetch objects whose keys end with this suffix (optional, default '')
        :param prune_key_prefix: Whether to omit key_prefix when appending key to target path (optional, default True)
        """
        finder: S3BucketObjectFinder = S3BucketObjectFinder(credentials=self.__credentials)
        s3_bucket_object_downloader: S3BucketObjectDownloader = S3BucketObjectDownloader(credentials=self.__credentials)
        for key in finder.get_matching_s3_keys(bucket, prefix=key_prefix, suffix=key_suffix):
            if prune_key_prefix and key.startswith(key_prefix):
                key_path = key[len(key_prefix):]  # removes key_prefix
            else:
                key_path = key
            target_path_and_name = os.path.join(target_path, key_path.strip('/'))
            s3_bucket_object_downloader.download(
                bucket, key, target_path_and_name, override_existing_file=override_existing_files)
