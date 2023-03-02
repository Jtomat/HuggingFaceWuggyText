from pydantic import BaseModel


class QuestionWithTextModel(BaseModel):
    question: str
    text: str
