import uvicorn


if __name__ == "__main__":
    uvicorn.run(
        "weather_api.app:api", host="0.0.0.0", port=8000, log_level="debug", reload=True
    )
