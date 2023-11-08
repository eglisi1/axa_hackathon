from pydantic import BaseModel


class Request(BaseModel):
    situation: str
