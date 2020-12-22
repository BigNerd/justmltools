from unittest import TestCase
from unittest.mock import MagicMock, patch


class TestS3Downloader(TestCase):

    @patch('justmltools.s3.aws_credentials.AwsCredentials')
    @patch('justmltools.s3.s3_bucket_object_downloader.S3BucketObjectDownloader')
    @patch('justmltools.s3.s3_bucket_object_finder.S3BucketObjectFinder')
    def test_download(
        self,
        s3_bucket_object_finder_mock: MagicMock,
        s3_bucket_object_downloader_mock: MagicMock,
        aws_credentials_mock: MagicMock,
    ):
        found_keys = ["one", "two"]
        s3_bucket_object_finder_mock.return_value.get_matching_s3_keys.return_value = found_keys

        from justmltools.s3.s3_downloader import S3Downloader
        sut = S3Downloader(credentials=aws_credentials_mock)
        sut.download(bucket="", target_path="")

        s3_bucket_object_finder_mock.assert_called_once()
        s3_bucket_object_finder_mock.return_value.get_matching_s3_keys.assert_called_once()
        self.assertEqual(len(found_keys), s3_bucket_object_downloader_mock.return_value.download.call_count)
