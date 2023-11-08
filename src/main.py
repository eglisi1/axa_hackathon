from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from util.logger import get_logger
from util.config import load_config
from model.request import Request
from model.response import Response

from service.analysis_service import AnalysisService

app = FastAPI()

# util
config = load_config("config/cfg.yaml")
logger = get_logger(__name__, config)

# services
anaysis_service = AnalysisService(config)

@app.get("/config")
def read_config() -> dict:
    return config


@app.put("/predict")
def predict(request: Request) -> Response:
    try:
        logger.info(f"Received request: {request}")
        analyzed_situation = anaysis_service.analyze_incident(request.situation)
        logger.info(f'analyzed situation: {analyzed_situation}')
        return Response(text=request.situation)
        # Analysis Service (analysis_service.py)
        # Legal Search Service (legal_search_service.py)
        # Compliance Check Service (compliance_service.py)
        # Liability Determination Service (liability_service.py)
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.exception_handler(404)
async def custom_404_handler(request: Request, exc):
    logger.error(f"404 error encountered: {request.url.path}")
    return JSONResponse(
        status_code=404,
        content={
            "message": f"Oops! The endpoint '{request.url.path}' does not exist. Please read the docs '/docs'."
        }
    )
