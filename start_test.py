# Импорты: тестовый клиент и экземпляр самого приложения
from fastapi.testclient import TestClient
from api import app

# Создаем экземпляр тестового клиента на базе приложения
client = TestClient(app)


def test_read_main():
    """
    Метод для проверки обработчика ошибок на методе получения списка статей
    """
    # Создаем запрос на нужный узел, без указания параметра
    response = client.get("/")
    # Проверяем, что сам ответ пришел без ошибок
    assert response.status_code == 200
    # Проверяем, что содержимое ответа ошибка
    assert response.json() == {"result": "error",
                               "message": "add 'q' parameter to request"}


def test_read_main_params():
    """Метод для проверки получения списка статей"""
    # Создаем запрос на нужный узел и указываем параметр
    response = client.get("/?q=keanu")
    # Проверяем, что сам ответ пришел без ошибок
    assert response.status_code == 200
    # Извлекаем содержимое ответа
    answer = response.json()
    # Проверяем, что ответ обработан
    assert answer["result"] == 'success'
    # Проверяем, что ответ содержит запись: 'Keanu Reeves'
    assert 'Keanu Reeves' in answer["data"]


def test_check_not_found_articles():
    """Метод для проверки получения списка статей при отсутсвии совпадений"""
    # Создаем запрос на нужный узел и указываем параметр
    response = client.get('/?q="     "')
    # Проверяем, что сам ответ пришел без ошибок
    assert response.status_code == 200
    # Проверяем, что ответ не содержит записей, а только сообщение
    assert response.json() == {"result": "success",
                               "message": "0 articles waw found"}


def test_ask_keanu():
    """"Метод для проверки получения ответа на вопрос"""
    # Создаем запрос на нужный узел и указываем параметр
    response = client.get("/ask?title=Keanu%20Reeves&question=when%20was"
                          "%20born%20Keanu%20Reeves")
    # Проверяем, что сам ответ пришел без ошибок
    assert response.status_code == 200
    # Проверяем, что строка в ответе содержит нужную дату
    assert "1997" in response.json()["data"]["answer"]


def test_check_russian_search():
    """"
    Метод для проверки получения списка статей,
    с использованием русского языка
    """
    # Создаем запрос на нужный узел и указываем параметр
    response = client.get("/?q=Пушкин")
    # Проверяем, что сам ответ пришел без ошибок
    assert response.status_code == 200
    # Извлекаем содержимое ответа
    answer = response.json()
    # Проверяем, что ответ обработан
    assert answer["result"] == 'success'
    # Проверяем, что ответ содержит запись: 'Alexander Pushkin'
    assert 'Alexander Pushkin' in answer["data"]


def test_check_summary_request():
    data = {
        "text": "The tower is 324 metres (1,063 ft) tall, about the "
                "same height as an 81-storey building, and the "
                "tallest structure in Paris. Its base is square, "
                "measuring 125 metres (410 ft) on each side. During "
                "its construction, the Eiffel Tower surpassed the "
                "Washington Monument to become the tallest man-made "
                "structure in the world, a title it held for 41 "
                "years until the Chrysler Building in New York City "
                "was finished in 1930. It was the first structure "
                "to reach a height of 300 metres. Due to the "
                "addition of a broadcasting aerial at the top of "
                "the tower in 1957, it is now taller than the "
                "Chrysler Building by 5.2 metres (17 ft). Excluding "
                "transmitters, the Eiffel Tower is the second "
                "tallest free-standing structure in France after "
                "the Millau Viaduct.",
        "min_length": 10,
        "max_length": 50
    }

    response = client.post("/make-text-abstract", json=data)
    assert response.status_code == 200
    res_data = response.json()
    summary = res_data["data"]["summary"]
    assert summary and len(summary) > 0
