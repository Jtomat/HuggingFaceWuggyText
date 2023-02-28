# Импорты: тестовый клиент и экземпляр самого приложения
from fastapi.testclient import TestClient
from api import app

# Создаем экземпляр тестового клиента на базе приложения
client = TestClient(app)


def test_read_main():
    """Метод для проверки обработчика ошибок на методе получения списка статей"""
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
    response = client.get("/ask?title=Keanu%20Reeves&question=when%20was%20born%20Keanu%20Reeves")
    # Проверяем, что сам ответ пришел без ошибок
    assert response.status_code == 200
    # Проверяем, что строка в ответе содержит нужную дату
    assert "1997" in response.json()["data"]["answer"]


def test_check_russian_search():
    """"Метод для проверки получения списка статей, с использованием русского языка"""
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
