### **Как запустить тесты:**

Клонировать репозиторий и перейти внутри него в директорию ```/tests```:
```
git clone https://github.com/8ubble8uddy/movies-async-api.git
```
```
cd movies-async-api/tests/
```

Создать файл .env и добавить настройки для тестов:
```
nano .env
```
```
# Elasticsearch
ELASTIC_HOST=elastic
ELASTIC_PORT=9200

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Service
URL_DOMAIN=fastapi
```

Развернуть и запустить тесты в контейнерах:
```
docker-compose up --build --exit-code-from tests
```

### Автор: Герман Сизов