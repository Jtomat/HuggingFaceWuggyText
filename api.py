# Для правльно обработки аннотаций и версий
from __future__ import annotations
# Базовые импорты: апи-сервер, пайплайн, загрузщик вики
from fastapi import FastAPI
from transformers import pipeline
import wikipedia


# Создаем экземпляр сервера
app = FastAPI()
# Устанавливаем тип обработки для пайплайна
classifier = pipeline("sentiment-analysis")
# Загружаем модель question-answering
pipe = pipeline("question-answering", model="AlexKay/xlm-roberta-large-qa"
                                            "-multilingual-finedtuned-ru")


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
