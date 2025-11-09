# CRUD Service

Простой CRUD сервис на FastAPI с чистой архитектурой и MongoDB.

## Структура проекта

Проект следует принципам чистой архитектуры:

```
src/
├── domain/              # Доменные модели
│   └── user.py         # Модели User, UserCreate, UserUpdate
├── usecase/            # Бизнес-логика
│   ├── user_repository.py      # Интерфейс репозитория
│   └── user_interactor.py      # Use case для работы с пользователями
├── infrastructure/     # Реализация инфраструктуры
│   ├── mongodb.py              # Подключение к MongoDB
│   └── user_repository_impl.py # Реализация репозитория для MongoDB
└── interfaces/         # API слой
    └── api/
        └── user_controller.py  # REST API контроллеры
```

## Зависимости

- **FastAPI** - веб-фреймворк
- **Motor** - асинхронный драйвер для MongoDB
- **Pydantic** - валидация данных
- **Uvicorn** - ASGI сервер

## Запуск

### Локально

1. Установите зависимости:
```bash
uv sync
```

2. Убедитесь, что MongoDB запущена (или используйте docker-compose)

3. Запустите приложение:
```bash
uv run python main.py
```

### Docker Compose

```bash
docker-compose up
```

Приложение будет доступно по адресу: `http://localhost:8080`

## API Endpoints

### Пользователи

- `POST /users/` - Создать пользователя
- `GET /users/` - Получить всех пользователей
- `GET /users/{user_id}` - Получить пользователя по ID
- `PUT /users/{user_id}` - Обновить пользователя
- `DELETE /users/{user_id}` - Удалить пользователя

### Другие endpoints

- `GET /` - Информация о сервисе
- `GET /health` - Проверка здоровья сервиса
- `GET /docs` - Swagger документация (автоматически генерируется FastAPI)

## Примеры запросов

### Создать пользователя

```bash
POST /users/
Content-Type: application/json

{
  "name": "Иван Иванов",
  "email": "ivan@example.com",
  "age": 25
}
```

### Получить всех пользователей

```bash
GET /users/
```

### Получить пользователя по ID

```bash
GET /users/{user_id}
```

### Обновить пользователя

```bash
PUT /users/{user_id}
Content-Type: application/json

{
  "name": "Иван Петров",
  "age": 26
}
```

### Удалить пользователя

```bash
DELETE /users/{user_id}
```

## Переменные окружения

- `MONGODB_URI` - URI подключения к MongoDB (по умолчанию: `mongodb://localhost:27017/crud_db`)

## Архитектура

Проект использует чистую архитектуру с разделением на слои:

1. **Domain** - доменные модели и бизнес-правила
2. **Use Case** - бизнес-логика и интерфейсы репозиториев
3. **Infrastructure** - реализация репозиториев и подключение к БД
4. **Interfaces** - REST API контроллеры

Это позволяет легко тестировать код и заменять реализации (например, заменить MongoDB на другую БД).

