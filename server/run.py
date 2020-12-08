import uvicorn

from weather_api import settings

if __name__ == "__main__":
    uvicorn.run(
        "weather_api.app:api",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
        log_config=settings.LOGGING_CONFIG,
    )
