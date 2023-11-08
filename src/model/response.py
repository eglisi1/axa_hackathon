from typing import List

from pydantic import BaseModel

from src.model.article_evaluation import ArticleEvaluation


class Response(BaseModel):
    artile_evaluations: List[ArticleEvaluation]
