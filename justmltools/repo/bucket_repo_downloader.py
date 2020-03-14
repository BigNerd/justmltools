from justmltools.config.local_data_path_config import LocalDataPathConfig
from justmltools.config.bucket_data_path_config import BucketDataPathConfig
from justmltools.repo.abstract_repo_downloader import AbstractRepoDownloader
from justmltools.s3.aws_credentials import AwsCredentials
from justmltools.s3.s3_bucket_object_downloader import S3BucketObjectDownloader


class BucketRepoDownloader(AbstractRepoDownloader):

    def __init__(
            self,
            local_data_path_config: LocalDataPathConfig,
            remote_data_path_config: BucketDataPathConfig,
            bucket: str,
            aws_credentials: AwsCredentials):
        super().__init__(local_data_path_config=local_data_path_config, remote_data_path_config=remote_data_path_config)
        self.__aws_credentials = aws_credentials
        self.__bucket = bucket

    def _download_object(self, remote_path: str, target_path: str):
        downloader: S3BucketObjectDownloader = self.__get_s3_bucket_object_downloader()
        downloader.download(
            bucket=self.__bucket,
            key=remote_path,
            target_path_and_name=target_path,
            override_existing_file=True
        )

    def __get_s3_bucket_object_downloader(self) -> S3BucketObjectDownloader:
        s3_bucket_object_downloader: S3BucketObjectDownloader = \
            S3BucketObjectDownloader(credentials=self.__aws_credentials)
        return s3_bucket_object_downloader
