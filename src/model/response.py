from pydantic import BaseModel


class Response(BaseModel):
    text: str
