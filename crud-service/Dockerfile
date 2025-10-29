# Этап сборки
FROM golang:1.24-alpine AS builder

WORKDIR /app

# Установка необходимых инструментов
RUN apk add --no-cache git

# Копирование файлов зависимостей
COPY go.mod go.sum ./
RUN go mod download

# Установка swag для генерации Swagger документации
RUN go install github.com/swaggo/swag/cmd/swag@latest

# Копирование исходного кода
COPY . .

# Обновление зависимостей и go.sum после копирования исходников
RUN go mod tidy

# Генерация Swagger документации
RUN swag init

# Сборка приложения
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

# Финальный образ
FROM alpine:latest

RUN apk --no-cache add ca-certificates

WORKDIR /root/

# Копирование скомпилированного приложения из builder
COPY --from=builder /app/main .

EXPOSE 8080

CMD ["./main"]
