from unittest import TestCase
from unittest.mock import MagicMock, patch


class TestS3BucketObjectFinder(TestCase):

    @patch('boto3.client')
    @patch('justmltools.s3.aws_credentials.AwsCredentials', autospec=True)
    def test_get_matching_s3_objects(
        self,
        aws_credentials_mock: MagicMock,
        client_mock: MagicMock,
    ):
        from types import GeneratorType
        from justmltools.s3.s3_bucket_object_finder import S3BucketObjectFinder
        sut = S3BucketObjectFinder()
        result = sut.get_matching_s3_objects(bucket="")
        self.assertIsInstance(result, GeneratorType)

    @patch('boto3.client')
    @patch('justmltools.s3.aws_credentials.AwsCredentials', autospec=True)
    def test_get_matching_s3_keys(
        self,
        aws_credentials_mock: MagicMock,
        client_mock: MagicMock,
    ):
        from types import GeneratorType
        from justmltools.s3.s3_bucket_object_finder import S3BucketObjectFinder
        sut = S3BucketObjectFinder()
        result = sut.get_matching_s3_keys(bucket="")
        self.assertIsInstance(result, GeneratorType)
