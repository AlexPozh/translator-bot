from environs import Env

from dataclasses import dataclass


env: Env = Env()
env.read_env()


@dataclass
class TelegramBotConfig:
    tg_token: str


@dataclass
class DataBaseConfig:
    drivername: str
    username: str
    password: str
    host: str
    database: str


@dataclass
class ApiConfig:
    content_type: str
    x_rapidAPI_key: str
    x_rapidAPI_host: str


def get_bot_config() -> TelegramBotConfig:
    return TelegramBotConfig(tg_token=env('BOT_TOKEN'))


def get_database_config() -> DataBaseConfig:
    return DataBaseConfig(
        drivername=env("drivername"),
        username=env("username"),
        password=env("password"),
        host=env("host"),
        database=env("database")
    )


def get_api_config() -> ApiConfig:
    return ApiConfig(
        content_type=env('CONTENT_TYPE'),
        x_rapidAPI_key=env('X_RAPID_API_KEY'),
        x_rapidAPI_host=env('X_RAPID_API_HOST')
    )
