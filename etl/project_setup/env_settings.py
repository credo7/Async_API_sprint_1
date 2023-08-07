import logging
from pydantic_settings import BaseSettings


logging.basicConfig(level=logging.INFO)


class Settings(BaseSettings):
    database_hostname: str
    database_port: int
    database_password: str
    database_name: str
    database_username: str
    redis_host: str
    redis_port: int
    elastic_host: str
    elastic_port: int
    elastic_scheme: str
    repeat_time_seconds: int

    @property
    def elastic_url(self):
        return f'{self.elastic_scheme}://{self.elastic_host}:{self.elastic_port}'

    @property
    def database_url(self):
        return f'postgresql://{self.database_username}:{self.database_password}@{self.database_hostname}:{self.database_port}/{self.database_name}'

    @property
    def redis_url(self):
        return f'redis://{self.redis_host}:{self.redis_port}/0'

    class Config:
        env_file = '../.env'
