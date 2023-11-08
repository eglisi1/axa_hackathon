from typing import List

from pydantic import BaseModel

from model.involved_party import InvolvedParty



class Response(BaseModel):
    involved_parties: List[InvolvedParty]
