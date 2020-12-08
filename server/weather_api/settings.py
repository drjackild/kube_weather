from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

HOST = config("APP_HOST", default="0.0.0.0")
PORT = config("APP_PORT", cast=int, default=8000)
DEBUG = config("APP_DEBUG", cast=bool, default=False)
OWM_API_KEY = config("APP_OWM_API_KEY", cast=Secret)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(asctime)s [%(levelname)s]: %(message)s",
            "use_colors": None,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(asctime)s [%(levelname)s]: %(client_addr)s - "%(request_line)s" %(status_code)s',  # noqa: E501
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "uvicorn": {"handlers": ["default"], "level": "INFO"},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
        "fastapi": {"handlers": ["default"], "level": "INFO"},
    },
}
