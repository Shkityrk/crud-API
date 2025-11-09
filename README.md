## CRUD сервис (на голанге)

CRUD по пользователям с чистой архитектурой, Swagger UI и проксированием через Nginx.

### Стек
- Go 1.24 (`crud-service`)
- MongoDB 7 (`mongodb`)
- Docker Compose
- Nginx (https, прокси для API и Swagger)
- Swagger UI (`/swagger/index.html`)

### Структура
- `crud-service/` — Go‑сервис (API)
- `nginx-service/` — конфигурация Nginx (SSL, прокси)
- `docker-compose.yml` — оркестрация сервисов
- `client/dist` — статика для Nginx (опционально)
- `environment/.env` — переменные окружения (опционально)

### Переменные окружения
Необходимо создать файл `environment/.env` . 
Пример:
```
MONGODB_URI=mongodb://mongodb:27017/crud_db
PORT=8080
```


### Запуск
```bash
docker compose up --build
```

После запуска:
- Swagger UI (через Nginx, https): https://localhost/swagger/index.html
- API: http://localhost:8080/
- Прямой доступ к Swagger (минуя Nginx): http://localhost:8080/swagger/index.html

### Эндпоинты
- POST `/users` — создать пользователя
- GET `/users` — список пользователей
- GET `/users/{id}` — получить по ID
- PUT `/users/{id}` — обновить
- DELETE `/users/{id}` — удалить

Модель `User`:
```json
{
  "id": 1,
  "name": "Иван Иванов",
  "email": "ivan@example.com",
  "age": 25,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Swagger
- Спецификация генерируется из аннотаций (swaggo).
- Генерация (локально):
```bash
cd crud-service
go run github.com/swaggo/swag/cmd/swag@latest init
```
