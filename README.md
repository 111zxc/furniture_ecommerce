# furniture_ecommerce
Веб-приложение на тему "Электронная коммерция подержанной мебели"

## Структура проекта
1. **REST API Gateway** - сервис, предоставляющий RESTful API для взаимодействия с клиентами. Обрабатывает внешние запросы и направляет соответствующим микросервисам.
2. **gRPC Users** - сервис, отвечающий за управление данными пользователей системы. Использует свой инстанц Postgre для хранения данных.
3. **gRPC Auth** - сервис, отвечающий за генерацию, расшифровку и верификацию JWT токенов. Нужен для авторизации действий пользователей. Использует свой Redis инстанц для хранения блэклиста revoked токенов.
4. **gRPC Product** - сервис, отвечающий за управление данными о продуктах. Использует свой инстанц Mongo для хранения данных.
5. **gRPC chat** - todo
6. **front** - todo

## Использование
Для инициализации баз данных:
1. `git clone github.com/111zxc/furniture_ecommerce`
2. `cd furniture_ecommerce`
3. `docker-compose up`

Для каждого сервиса:
1. `cd <service_dir>`
2. `python -m venv env`
3. `/env/Scripts/activate.ps1` или `\env\Scripts\activate`
4. `pip install -r requirements.txt`
5. `python main.py`
