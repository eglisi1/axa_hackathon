from util.logger import get_logger
from typing import Union
from fastapi import FastAPI
from util.logger import load_config
from model.request import Request

app = FastAPI()

config_path = "config/cfg.yaml"
logger = get_logger(__name__, config_path)
config = load_config(config_path)


@app.get("/config")
def read_config():
    return config


@app.put("/predict")
def read_item(request: Request) -> str:
    logger.info(f"Received request: {request}")
    return 'prediction'
