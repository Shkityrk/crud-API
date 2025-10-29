## CRUD сервис (Go + MongoDB + Docker + Nginx)

Минималистичный CRUD по пользователям с чистой архитектурой, Swagger UI и проксированием через Nginx.

### Стек
- Go 1.24 (модуль в `crud-service`)
- MongoDB 7 (контейнер `mongodb`)
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
Файл `environment/.env` (необязательно). Пример:
```
MONGODB_URI=mongodb://mongodb:27017/crud_db
PORT=8080
```
Примечание: `docker-compose.yml` уже задаёт `MONGODB_URI` по умолчанию на внутренний хост `mongodb`.

### Запуск
```bash
docker compose down -v
docker compose up --build
```

После запуска:
- API: http://localhost:8080/
- Swagger UI (через Nginx, https): https://localhost/swagger/index.html
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
  "id": 1,                 // int64, автоинкремент
  "name": "Иван Иванов",
  "email": "ivan@example.com",
  "age": 25,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

Автоинкремент ID реализован через коллекцию `counters` в MongoDB (`_id: "users"`, поле `seq`).

### Swagger
- Спецификация генерируется из аннотаций (swaggo).
- Генерация (локально):
```bash
cd crud-service
go run github.com/swaggo/swag/cmd/swag@latest init
```

### CORS и HTTPS
- Nginx слушает 80/443, редирект с 80 на 443.
- В `nginx-service/nginx.conf` включены CORS‑заголовки для `/users` и `/swagger`.
- Swagger настроен на `https` в `crud-service/main.go`.

### Тривиальный локальный запуск без Docker
Требуется локальный MongoDB на 27017.
```powershell
$env:MONGODB_URI="mongodb://localhost:27017/crud_db"
cd crud-service
go run .
```
Swagger: http://localhost:8080/swagger/index.html

### Частые проблемы
- "Failed to connect to MongoDB" внутри контейнера:
  - Проверьте, что используется `MONGODB_URI=mongodb://mongodb:27017/crud_db` (внутренний хост `mongodb`).
  - Убедитесь, что `mongodb` имеет статус `healthy`:
    ```bash
    docker compose ps
    docker compose logs mongodb
    ```
- Swagger "Failed to fetch" при открытии через https:
  - Используйте `https://localhost/swagger/index.html`.
  - Проверьте CORS‑заголовки в `nginx-service/nginx.conf` и `docs.SwaggerInfo.Schemes = ["https"]` в `crud-service/main.go`.

### Разработка
```bash
cd crud-service
go mod tidy
go test ./...
go run .
```


