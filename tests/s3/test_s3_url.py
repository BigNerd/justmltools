from unittest import TestCase

from justmltools.s3.s3_url import S3Url


class TestS3Url(TestCase):

    def test_init(self):
        sut = S3Url(bucket="my_test_bucket", key="my_test_key")
        self.assertEqual("my_test_bucket", sut.bucket)
        self.assertEqual("my_test_key", sut.key)

    def test_parse_from(self):
        sut: S3Url = S3Url.parse_from("s3://my_test_bucket/my_test_key")
        self.assertEqual("my_test_bucket", sut.bucket)
        self.assertEqual("my_test_key", sut.key)
