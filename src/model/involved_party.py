from typing import List

from pydantic import BaseModel

from model.article_evaluation import ArticleEvaluation


class InvolvedParty(BaseModel):
    name: str
    vehicle: str
    article_evaluations: List[ArticleEvaluation]