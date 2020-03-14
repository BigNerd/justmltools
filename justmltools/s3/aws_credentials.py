class AwsCredentials:

    def __init__(self, aws_secret_access_key_id: str, aws_secret_access_key: str, region_name: str):
        self.__aws_secret_access_key_id: str = aws_secret_access_key_id
        self.__aws_secret_access_key: str = aws_secret_access_key
        self.__region_name: str = region_name

    @property
    def aws_secret_access_key_id(self):
        return self.__aws_secret_access_key_id

    @property
    def aws_secret_access_key(self):
        return self.__aws_secret_access_key

    @property
    def region_name(self):
        return self.__region_name
