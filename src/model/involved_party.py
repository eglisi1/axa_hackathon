from typing import List

from pydantic import BaseModel

from src.model.article_evaluation import ArticleEvaluation


class InvolvedParty(BaseModel):
    name: str
    vehicle: str
    article_evaluations: List[ArticleEvaluation]