import pathlib
import urllib.parse
import requests

from justmltools.repo.abstract_repo_downloader import AbstractRepoDownloader
from justmltools.config.local_data_path_config import LocalDataPathConfig
from justmltools.config.gitlab_data_path_config import GitlabDataPathConfig


class GitlabRepoDownloader(AbstractRepoDownloader):

    def __init__(
            self,
            local_data_path_config: LocalDataPathConfig,
            remote_data_path_config: GitlabDataPathConfig,
            host: str,
            access_token: str,
            project_id: str,
            ref: str = "main",
    ):
        super().__init__(local_data_path_config=local_data_path_config, remote_data_path_config=remote_data_path_config)
        self.__host = host
        self.__access_token = access_token
        self.__project_id = project_id
        self.__ref = ref

    def _download_object(self, remote_path: str, target_path: str):
        headers = {"PRIVATE-TOKEN": self.__access_token}
        url_encoded_remote_path = urllib.parse.quote(remote_path, safe="")
        url = f"https://{self.__host}/api/v4/projects/{self.__project_id}/" \
              f"repository/files/{url_encoded_remote_path}/raw?ref={self.__ref}"
        print(f"downloading {url} ...")
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            self._save_as_file(file_content=r.text, target_path=target_path)
        else:
            raise Exception(f"Could not download {url}, received status code: {r.status_code}")

    @staticmethod
    def _save_as_file(file_content: str, target_path):
        pathlib.Path(pathlib.Path(target_path).parent).mkdir(parents=True, exist_ok=True)
        with open(target_path, "w") as text_file:
            text_file.write(file_content)
