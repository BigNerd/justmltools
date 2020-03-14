import urllib.parse


class S3Url:

    def __init__(self, bucket: str, key: str = None):
        self.__bucket = bucket
        self.__key = key

    @staticmethod
    def parse_from(url_string: str):
        if not url_string.startswith("s3://"):
            url_string = "s3://" + url_string
        components = urllib.parse.urlparse(url_string)
        scheme = components.scheme
        if scheme == 's3':
            bucket = components.netloc
            key = components.path
            if key is not None:
                key = key.lstrip('/')
            return S3Url(bucket, key)
        else:
            raise ValueError(f"Invalid S3 url {url_string}, must start with s3://")

    @property
    def bucket(self) -> str:
        return self.__bucket

    @property
    def key(self) -> str:
        return self.__key
