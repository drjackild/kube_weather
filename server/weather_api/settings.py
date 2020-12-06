from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

DEBUG = config("APP_DEBUG", cast=bool, default=False)
OWM_API_KEY = config("APP_OWM_API_KEY", cast=Secret)
