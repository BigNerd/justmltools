from unittest import TestCase
from unittest.mock import MagicMock, patch


class TestS3BucketObjectUploader(TestCase):

    @patch('boto3.resource')
    @patch('justmltools.s3.aws_credentials.AwsCredentials', autospec=True)
    def test_upload(
        self,
        aws_credentials_mock: MagicMock,
        resource_mock: MagicMock,
    ):
        from justmltools.s3.s3_bucket_object_uploader import S3BucketObjectUploader
        sut = S3BucketObjectUploader()
        sut.upload(source_path_and_name="", bucket="", key="")
        resource_mock.return_value.Bucket.return_value.upload_file.assert_called_once()
