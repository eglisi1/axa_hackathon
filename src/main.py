from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from util.logger import get_logger
from util.config import load_config
from model.request import Request
from model.response import Response

from service.analysis_service import AnalysisService
from service.law_evaluation_service import LawEvaluationService

app = FastAPI()

# util
config = load_config("config/cfg.yaml")
logger = get_logger(__name__, config)

# services
analysis_service = AnalysisService(config)
compliance_service = LawEvaluationService(config)


@app.get("/config")
def read_config() -> dict:
    return config


@app.put("/predict")
def predict(request: Request) -> Response:
    try:
        logger.info(f"Received request: {request}")
        analyzed_situation = analysis_service.analyze_incident(request.situation)
        logger.info(f'analyzed situation: {analyzed_situation}')
        
        # Legal Search Service (legal_search_service.py)

        # TODO: enable if input dict is ready!
        # article_evaluations = compliance_service.evaluate_laws(input)

        # Liability Determination Service (liability_service.py)

        # TODO: add article_evaluations when input is ready
        return Response(artile_evaluations=[])
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
