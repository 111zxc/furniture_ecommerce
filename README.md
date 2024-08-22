# furniture_ecommerce
Веб-приложение на тему "Электронная коммерция подержанной мебели"

## Структура проекта
1. **REST API Gateway** - сервис, предоставляющий RESTful API для взаимодействия с клиентами. Обрабатывает внешние запросы и направляет соответствующим микросервисам.
2. **gRPC Users** - сервис, отвечающий за управление данными пользователей системы. Использует свой инстанц Postgre для хранения данных.
3. **gRPC Auth** - сервис, отвечающий за генерацию, расшифровку и верификацию JWT токенов. Нужен для авторизации действий пользователей. Использует свой Redis инстанц для хранения блэклиста revoked токенов.
4. **gRPC Product** - сервис, отвечающий за управление данными о продуктах. Использует свой инстанц Mongo для хранения данных.
