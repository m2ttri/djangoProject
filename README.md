Для запуска приложения:
- Создайте виртуальное окружение
- Обновите менеджер пакетов: python.exe -m pip install --upgrade pip
- Установите все зависимости: pip install -r requirements.txt
- Примените миграции: python manage.py migrate
- Запустите сервер: python manage.py runserver


Модели база данных: learning/models.py

Реализация API: learning/api/


получить список продуктов: GET 127.0.0.1:8000/api/products/ 

получить список уроков по id продукта: GET 127.0.0.1:8000/api/products/*id*/lessons