# Для правльно обработки аннотаций и версий
from __future__ import annotations
# Базовые импорты: апи-сервер, пайплайн, загрузщик вики
from fastapi import FastAPI
from transformers import pipeline
import wikipedia
import translators.server as ts

from models import QuestionWithTextModel

# Создаем экземпляр сервера
app = FastAPI()
# Устанавливаем тип обработки для пайплайна
classifier = pipeline("sentiment-analysis")
# Загружаем модель question-answering
pipe = pipeline("question-answering", model="AlexKay/xlm-roberta-large-qa"
                                            "-multilingual-finedtuned-ru")
gpt2_pipe = pipeline('text-generation', model='gpt2')


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
                # иначе сообщение об отсутствии совпадений
                return {"result": "success",
                        "message": "0 articles waw found"}
    # Если даже q не указан в запросе, то возвращаем ошибку
    return {"result": "error", "message": "add 'q' parameter to request"}


@app.get("/ask")
def predict(title: str = None, question: str = None) -> dict:
    """
    Метод получения ответа из выбранной статьи

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


@app.post("/find-answer")
def find_answer_from_text(question_with_text: QuestionWithTextModel):
    """
    Метод получения ответа из передаваемого текста

    :param question_with_text: тело запроса,
    содержащее вопрос и текст, в котором нужно найти ответ
    :return: текст ответа
    """
    context = question_with_text.text
    question = question_with_text.question

    if context and question and context != "" and question != "":
        answer = pipe(question=question, context=context)
        return {"result": "success", "data": answer}
    return {"result": "error",
            "message": "property 'text' or 'question' in body are missed or empty"}


@app.get("/make-text")
def make_text_from_phrase(phrase: str = None, length: int = 100, translate: bool = False):
    """
    Метод генерации текстов по передаваемой фразе заданной длины.
    Генерируется 5 вариантов текста

    :param phrase: фраза, на основании которой будут сгенерированы тексты
    :param length: ограничение по длине текстов
    :param translate: маркер осуществления перевода
    :return: объект ответа. Значением свойства data является объект,
    где ключ - порядковый номер текста, значение - текст
    """
    if phrase:
        res = gpt2_pipe(phrase, max_length=length,
                        num_return_sequences=5)
        if len(res) > 0:
            data = {}
            for idx, item in enumerate(res):
                text = item["generated_text"]\
                    .replace('\"', '').replace('\n\n', ' ')
                if translate:
                    text = ts.google(text, from_language='en', to_language='ru')

                data.update({idx: text[0:text.rfind('.')+1]})
            return {"result": "success", "data": data}
        return {"result": "error",
                "message": "no one sentence wasn't generated"}
    return {"result": "error", "message": "lost 'phrase' param"}
