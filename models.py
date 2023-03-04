from pydantic import BaseModel


class TextSummaryModel(BaseModel):
    text: str
    num_beams: int = 2
    min_length: int = 0
    max_length: int = 100
