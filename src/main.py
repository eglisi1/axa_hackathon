from fastapi import FastAPI, HTTPException

from util.logger import get_logger
from util.config import load_config
from model.request import Request

app = FastAPI()

config = load_config("config/cfg.yaml")
logger = get_logger(__name__, config)


@app.get("/config")
def read_config() -> dict:
    return config


@app.put("/predict")
def predict(request: Request) -> Request:
    try:
        logger.info(f"Received request: {request}")
        return Request(text=request.text)
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
