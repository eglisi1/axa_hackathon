from fastapi import FastAPI

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
def read_item(request: Request) -> str:
    logger.info(f"Received request: {request}")
    return "prediction"
