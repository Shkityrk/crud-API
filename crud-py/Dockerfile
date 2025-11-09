FROM python:3.12-slim

WORKDIR /app

# Установка uv для управления зависимостями
RUN pip install --no-cache-dir uv

# Копирование файлов зависимостей
COPY pyproject.toml uv.lock ./

# Установка зависимостей
RUN uv sync --frozen

# Копирование исходного кода
COPY . .

EXPOSE 8080

# Запуск приложения через uv
CMD ["uv", "run", "python", "main.py"]
