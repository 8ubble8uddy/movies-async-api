## Movies Async Api

[![python](https://img.shields.io/static/v1?label=python&message=3.8%20|%203.9%20|%203.10&color=informational)](https://github.com/8ubble8uddy/movies-async-api/actions/workflows/main.yml)
[![dockerfile](https://img.shields.io/static/v1?label=dockerfile&message=published&color=2CB3E8)](https://hub.docker.com/r/8ubble8uddy/async_api)
[![last updated](https://img.shields.io/static/v1?label=last%20updated&message=september%202022&color=yellow)](https://img.shields.io/static/v1?label=last%20updated&message=november%202022&color=yellow)
[![lint](https://img.shields.io/static/v1?label=lint&message=flake8%20|%20mypy&color=brightgreen)](https://github.com/8ubble8uddy/movies-async-api/actions/workflows/main.yml)
[![code style](https://img.shields.io/static/v1?label=code%20style&message=WPS&color=orange)](https://wemake-python-styleguide.readthedocs.io/en/latest/)
[![tests](https://img.shields.io/static/v1?label=tests&message=%E2%9C%94%2015%20|%20%E2%9C%98%200&color=critical)](https://github.com/8ubble8uddy/movies-async-api/actions/workflows/main.yml)

### **Описание**

_Целью данного проекта является реализация асинхронного API для полнотекстового поиска фильмов. В связи с этим было разработано приложение на основе узкоспециализированного фреймворка [FastAPI](https://fastapi.tiangolo.com). В качестве хранилища используется поисковый движок [ElasticSearch](https://www.elastic.co). Чтобы не нагружать лишний раз систему полнотекстового поиска применяется кеширование данных с помощью [Redis](https://redis.io). Проект запускается под управлением сервера ASGI(uvicorn) в связке с HTTP-сервером [NGINX](https://nginx.org). Для проверки результата работы API написаны функциональный тесты с использованием библиотеки [pytest](https://pytest.org)._

### **Технологии**

```Python``` ```FastAPI``` ```Elasticsearch``` ```Redis``` ```NGINX``` ```Gunicorn``` ```PyTest``` ```Docker```

### **Как запустить проект:**

Клонировать репозиторий и перейти внутри него в директорию ```/infra```:
```
git clone https://github.com/8ubble8uddy/movies-async-api.git
```
```
cd movies-async-api/infra/
```

Создать файл .env и добавить настройки для проекта:
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
```

Развернуть и запустить проект в контейнерах:
```
docker-compose up
```

Документация API будет доступна по адресу:
```
http://127.0.0.1/openapi
```

### Автор: Герман Сизов