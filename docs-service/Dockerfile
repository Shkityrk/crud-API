FROM nginx:alpine

# Копирование HTML файла с Redoc
COPY index.html /usr/share/nginx/html/

# Копирование конфигурации nginx (опционально, если нужна кастомная)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

