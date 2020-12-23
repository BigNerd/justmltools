from unittest import TestCase
from unittest.mock import MagicMock, patch

from justmltools.s3.s3_bucket_object_downloader import S3BucketObjectDownloader
from justmltools.s3.aws_credentials import AwsCredentials


@patch('os.path.isdir', autospec=True, return_value=True)
@patch('os.path.isfile', autospec=True, return_value=True)
@patch('boto3.resource', autospec=True)
class TestS3BucketObjectDownloader(TestCase):

    def test_init(
            self,
            boto3_resource: MagicMock,
            os_path_is_file: MagicMock,
            os_path_is_dir: MagicMock
    ):
        sut = S3BucketObjectDownloader()

        sut = S3BucketObjectDownloader(
            credentials=AwsCredentials(
                aws_secret_access_key_id="test_id",
                aws_secret_access_key="test_key",
                region_name="test_region"
            )
        )
        self.assertEqual(2, boto3_resource.call_count)

    def test_download_with_no_override(
            self,
            boto3_resource: MagicMock,
            os_path_is_file: MagicMock,
            os_path_is_dir: MagicMock
    ):
        sut = S3BucketObjectDownloader()
        self.assertEqual(1, boto3_resource.call_count)
        with self.assertRaises(FileExistsError):
            sut.download(
                bucket="test_bucket",
                key="test_key",
                target_path_and_name="test_target_path",
                override_existing_file=False
            )
        self.assertEqual(1, boto3_resource.call_count)
        self.assertEqual(1, os_path_is_file.call_count)

    def test_download_with_override(
            self,
            boto3_resource: MagicMock,
            os_path_is_file: MagicMock,
            os_path_is_dir: MagicMock
    ):
        sut = S3BucketObjectDownloader()
        self.assertEqual(1, boto3_resource.call_count)
        sut.download(
            bucket="test_bucket",
            key="test_key",
            target_path_and_name="test_target_path",
            override_existing_file=True
        )
        self.assertEqual(1, boto3_resource.call_count)
        self.assertEqual(0, os_path_is_file.call_count)

    def test_download_dir_with_override(
            self,
            boto3_resource: MagicMock,
            os_path_is_file: MagicMock,
            os_path_is_dir: MagicMock
    ):
        sut = S3BucketObjectDownloader()
        self.assertEqual(1, boto3_resource.call_count)
        sut.download(
            bucket="test_bucket",
            key="test_key/",
            target_path_and_name="test_target_path",
            override_existing_file=True
        )
        self.assertEqual(1, boto3_resource.call_count)
        self.assertEqual(0, os_path_is_file.call_count)
        self.assertEqual(1, os_path_is_dir.call_count)
