from unittest import TestCase
from unittest.mock import Mock

from justmltools.repo.bucket_repo_downloader import BucketRepoDownloader
from justmltools.config.bucket_data_path_config import BucketDataPathConfig
from justmltools.config.local_data_path_config import LocalDataPathConfig


class TestBucketRepoDownloader(TestCase):

    def test_(self):
        _ = BucketRepoDownloader(
            local_data_path_config=LocalDataPathConfig(prefix="my_local_test_prefix"),
            remote_data_path_config=BucketDataPathConfig(prefix="my_bucket_test_prefix"),
            bucket="test_bucket",
            aws_credentials=Mock()
        )
