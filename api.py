# Для правльно обработки аннотаций и версий
from __future__ import annotations
# Базовые импорты: апи-сервер, пайплайн, загрузщик вики
from fastapi import FastAPI
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import wikipedia

from models import TextSummaryModel

# Создаем экземпляр сервера
app = FastAPI()
# Загружаем модель question-answering
pipe = pipeline("question-answering", model="AlexKay/xlm-roberta-large-qa"
                                            "-multilingual-finedtuned-ru")

tokenizer = AutoTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
abstract_text_model = AutoModelForSeq2SeqLM \
    .from_pretrained("sshleifer/distilbart-cnn-12-6")


@app.get("/")
def root(q: str = None) -> dict:
    """Метод получения списка статей из википедии
    
        q : str - Наименованние искомой статьи"""
    if q:
        # Защита от пустых запросов
        if q.strip() != "":
            # Создаем запрос и ждем ответа
            context = wikipedia.search(q)
            # Если нашли что-нибудь,
            if len(context) != 0:
                # то возвращаем в качестве ответа,
                return {"result": "success", "data": context}
            else:
                # иначе сообщение об отсутсвии совпадений
                return {"result": "success",
                        "message": "0 articles waw found"}
    # Если даже q не указан в запросе, то возвращаем ошибку
    return {"result": "error", "message": "add 'q' parameter to request"}


@app.get("/ask")
def predict(title: str = None, question: str = None) -> dict:
    """Метод получения ответа из выбранной статьи
    
    title: str = None - Точное наименование статьи
    question: str = None - Вопрос по содержимому статьи
    """
    # Защита от неполных запросов.
    if title and question:
        # Выводим в консоль сервера лог о статье и запросе
        print(title)
        print(question)
        # Запрашиваем и ожидаем содержание статьи
        context = wikipedia.search(title)
        # Выводим в консоль сервера лог о содержании статьи
        print('context', context)
        # Вытаскиваем только текстовые данные из статьи - это контекст
        article = wikipedia.page(context[0]).content
        # Запускам модель пайплайна для разбора текущей контекст статьи,
        # заодно передаем вопрос. Это будет долго...
        answer = pipe(question=question, context=article)
        # Возвращаем результат обработки
        return {"result": "success", "data": answer}
    # Возвращаем ошибку, если что-то не было указано.
    return {"result": "error", "message": "lost some params"}


@app.post("/make-text-abstract")
def make_text_abstract(text_obj: TextSummaryModel):
    """
     Метод для получения реферерато по передаваемому тексту

     :return объект ответа, где в свойстве data
     содержится реферат в поле summary
     """
    text = text_obj.text
    num_beams = text_obj.num_beams
    min_length = text_obj.min_length
    max_length = text_obj.max_length

    if max_length < min_length:
        return {"result": "error", "message": "property value  'max_length', "
                                              "should be more than value of "
                                              "property 'min_length'"}
    if text and text != "":
        inputs = tokenizer([text], max_length=1024,
                           return_tensors="pt")

        summary_ids = abstract_text_model\
            .generate(inputs["input_ids"],
                      num_beams=num_beams,
                      min_length=min_length,
                      max_length=max_length)

        summary = tokenizer\
            .batch_decode(summary_ids,
                          skip_special_tokens=True,
                          clean_up_tokenization_spaces=False)[0]

        return {"result": "success", "data": {"summary": summary}}
    return {"result": "error", "message": "property 'text' was missed"}
