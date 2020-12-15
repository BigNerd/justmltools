from unittest import TestCase
from unittest.mock import MagicMock, patch

from justmltools.s3.aws_credentials import AwsCredentials


class TestS3Copier(TestCase):

    @patch('boto3.resource')
    @patch('justmltools.s3.s3_bucket_object_finder.S3BucketObjectFinder')
    def test_copy_s3_objects(self, finder_mock: MagicMock, boto3_resource: MagicMock):
        from_prefix = "my/from/prefix"
        expected_from_keys = [f"{from_prefix}/x", f"{from_prefix}/y"]
        finder_mock.return_value.get_matching_s3_keys.return_value = expected_from_keys
        from justmltools.s3.s3_copier import S3Copier
        sut = S3Copier(
            credentials=AwsCredentials(
                aws_secret_access_key_id="test_id",
                aws_secret_access_key="test_key",
                region_name="test_region"
            )
        )

        to_prefix = "my/to/prefix"
        expected_to_keys = [key.replace(from_prefix, to_prefix) for key in expected_from_keys]
        actual_from_keys = []
        actual_to_keys = []
        for from_key, to_key in sut.copy_s3_objects(
                bucket="my_bucket", from_prefix="my/from/prefix", to_prefix="my/to/prefix"):
            actual_from_keys.append(from_key)
            actual_to_keys.append(to_key)
        self.assertEqual(expected_from_keys, actual_from_keys)
        self.assertEqual(expected_to_keys, actual_to_keys)
