from fastapi import FastAPI

api = FastAPI()


@api.get("/forecast")
async def get_forecast(lat: float, lon: float):
    return {"result": "OK"}
