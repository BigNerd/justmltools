from unittest import TestCase
from unittest.mock import MagicMock, patch

from justmltools.s3.s3_bucket_object_downloader import S3BucketObjectDownloader
from justmltools.s3.aws_credentials import AwsCredentials


def mocked_os_path_exists(path: str) -> bool:
    return True


def mocked_os_path_isdir(path: str) -> bool:
    return True


def mocked_os_path_isfile(path: str) -> bool:
    return True


def mocked_boto3_resource(resource_name: str, aws_access_key_id=None, aws_secret_access_key=None, region_name=None):
    return MagicMock()


class TestS3BucketObjectDownloader(TestCase):

    @patch('boto3.resource', side_effect=mocked_boto3_resource)
    def test_init(self, boto3_resource: MagicMock):
        sut = S3BucketObjectDownloader()
        sut = S3BucketObjectDownloader(
            credentials=AwsCredentials(
                aws_secret_access_key_id="test_id",
                aws_secret_access_key="test_key",
                region_name="test_region"
            )
        )
        self.assertEqual(2, boto3_resource.call_count)

    @patch('os.path.isfile', side_effect=mocked_os_path_isfile)
    @patch('boto3.resource', side_effect=mocked_boto3_resource)
    def test_download_with_no_override(
            self,
            boto3_resource: MagicMock,
            os_path_isfile_function: MagicMock):
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
        self.assertEqual(1, os_path_isfile_function.call_count)

    @patch('os.path.isfile', side_effect=mocked_os_path_isfile)
    @patch('boto3.resource', side_effect=mocked_boto3_resource)
    def test_download_with_override(
            self,
            boto3_resource: MagicMock,
            os_path_isfile_function: MagicMock):
        sut = S3BucketObjectDownloader()
        self.assertEqual(1, boto3_resource.call_count)
        sut.download(
            bucket="test_bucket",
            key="test_key",
            target_path_and_name="test_target_path",
            override_existing_file=True
        )
        self.assertEqual(1, boto3_resource.call_count)
        self.assertEqual(0, os_path_isfile_function.call_count)

    @patch('os.path.isdir', side_effect=mocked_os_path_isdir)
    @patch('os.path.isfile', side_effect=mocked_os_path_isfile)
    @patch('boto3.resource', side_effect=mocked_boto3_resource)
    def test_download_dir_with_override(
            self,
            boto3_resource: MagicMock,
            os_path_isfile_function: MagicMock,
            os_path_isdir_function: MagicMock):
        sut = S3BucketObjectDownloader()
        self.assertEqual(1, boto3_resource.call_count)
        sut.download(
            bucket="test_bucket",
            key="test_key/",
            target_path_and_name="test_target_path",
            override_existing_file=True
        )
        self.assertEqual(1, boto3_resource.call_count)
        self.assertEqual(0, os_path_isfile_function.call_count)
        self.assertEqual(1, os_path_isdir_function.call_count)
