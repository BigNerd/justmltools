from unittest import TestCase
from unittest.mock import MagicMock, patch


class TestS3Uploader(TestCase):

    @patch('justmltools.s3.aws_credentials.AwsCredentials')
    @patch('justmltools.s3.s3_bucket_object_uploader.S3BucketObjectUploader')
    def test_upload(
        self,
        s3_bucket_object_uploader_mock: MagicMock,
        aws_credentials_mock: MagicMock,
    ):
        source_file_paths = ["one", "two"]
        bucket = ""

        from justmltools.s3.s3_uploader import S3Uploader
        sut = S3Uploader(credentials=aws_credentials_mock)
        sut.upload(source_file_paths=source_file_paths, bucket=bucket)

        s3_bucket_object_uploader_mock.assert_called_once()
        self.assertEqual(len(source_file_paths), s3_bucket_object_uploader_mock.return_value.upload.call_count)
