from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from util.logger import get_logger
from util.config import load_config
from model.request import Request
from model.response import Response
from typing import List

from service.analysis_service import AnalysisService
from service.legal_search_service import LegalSearchService
from service.law_evaluation_service import LawEvaluationService
from service.double_check_service import DoubleCheckService

app = FastAPI()

# util
config = load_config("config/cfg.yaml")
logger = get_logger(__name__, config)

# services
analysis_service = AnalysisService(config)
legal_search_service = LegalSearchService(config)
double_check_service = DoubleCheckService(config)
compliance_service = LawEvaluationService(config)


@app.get("/config")
def read_config() -> dict:
    return config


@app.put("/predict")
def predict(request: Request) -> List:
    # todo return Response
    try:
        logger.info(f"Received request: {request}")
        analyzed_situation = analysis_service.analyze_incident(request.situation)
        logger.info(f'analyzed situation: {analyzed_situation}')
        situation_with_law = legal_search_service.search_relevant_articles(analyzed_situation)
        logger.info(f'situation with law: {situation_with_law}')
        situation_with_law_and_double_checked = double_check_service.double_check(situation_with_law)
        logger.info(f'situation with law and double checked: {situation_with_law_and_double_checked}')
        involved_parties = []
        for situation in situation_with_law_and_double_checked:
            article_evaluations = compliance_service.evaluate_laws(situation)
            logger.info(f'article evaluations: {article_evaluations}')
            involved_parties.append({
                "name": situation["beteiligter"],
                "vehicle": situation["fahrzeug"],
                "article_evaluations": article_evaluations
            })
        logger.info(f'involved parties: {involved_parties}')
        return involved_parties
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
