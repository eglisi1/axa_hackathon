from typing import List

from pydantic import BaseModel

from src.model.involved_party import InvolvedParty


class Response(BaseModel):
    involved_parties: List[InvolvedParty]
