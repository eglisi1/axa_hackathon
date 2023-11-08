from pydantic import BaseModel


class ArticleEvaluation(BaseModel):
    violation: bool
    reason: str
    article_id: str
    article_text: str