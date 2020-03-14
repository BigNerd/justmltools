from unittest import TestCase

from justmltools.s3.aws_credentials import AwsCredentials


class TestAwsCredentials(TestCase):

    def test_(self):
        sut = AwsCredentials(
            aws_secret_access_key_id="test_id",
            aws_secret_access_key="test_key",
            region_name="test_region"
        )
        self.assertEqual("test_id", sut.aws_secret_access_key_id)
        self.assertEqual("test_key", sut.aws_secret_access_key)
        self.assertEqual("test_region", sut.region_name)
