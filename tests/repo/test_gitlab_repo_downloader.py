from unittest import TestCase

from justmltools.repo.gitlab_repo_downloader import GitlabRepoDownloader
from justmltools.config.gitlab_data_path_config import GitlabDataPathConfig
from justmltools.config.local_data_path_config import LocalDataPathConfig


class TestGitlabRepoDownloader(TestCase):

    def test_(self):
        _ = GitlabRepoDownloader(
            local_data_path_config=LocalDataPathConfig(prefix="my_local_test_prefix"),
            remote_data_path_config=GitlabDataPathConfig(),
            access_token="",
            project_id="",
            host="",
        )
