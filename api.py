from __future__ import annotations

from fastapi import FastAPI
from transformers import pipeline
import wikipedia
from typing import Union
from pydantic import BaseModel


class Item(BaseModel):
    text: str


app = FastAPI()
classifier = pipeline("sentiment-analysis")
pipe = pipeline("question-answering", model="AlexKay/xlm-roberta-large-qa"
                                            "-multilingual-finedtuned-ru")


@app.get("/")
def root(q: str = None):
    if q:
        if q.strip() != "":
            context = wikipedia.search(q)
            if len(context) != 0:
                return {"result": "success", "data": context}
            else:
                return {"result": "success",
                        "message": "0 articles waw found"}

    return {"result": "error", "message": "add 'q' parameter to request"}


@app.get("/ask")
def predict(title: str = None, question: str = None):
    if title and question:
        print(title)
        print(question)
        context = wikipedia.search(title)
        print('context', context)
        article = wikipedia.page(context[0]).content
        answer = pipe(question=question, context=article)
        return {"result": "success", "data": answer}
    return {"result": "error", "message": "lost some params"}
