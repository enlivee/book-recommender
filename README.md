# Book Recommender (Читательский дневник с ИИ-подбором)

## 1. Идея проекта

Пользователь ведет дневник прочитанных книг с оценками и отзывами. На основе его предпочтений система автоматически подбирает книги из каталога с помощью семантического поиска (pgvector). Рекомендации генерируются асинхронно, не блокируя интерфейс.        

## 2. Основные функции
    - Добавление прочитанных книг
    - Отзыв о книге, оценка
    - Автоматический подбор рекомендованных книг по предпочтениям

## 3. Архитектура (как система работает)

Сценарий 1. 

        Пользователь → POST /api/books (FastAPI)
      → Сервис сохраняет книгу в PostgreSQL
      → Возвращает 201 Created

Сценарий 2.

        Пользователь → POST /api/recommendations (FastAPI)
      → FastAPI создает задачу в RabbitMQ
      → FastAPI сразу отвечает 202 Accepted с task_id
      → Celery Worker забирает задачу:
          → Берет историю пользователя из PostgreSQL
          → Ищет похожие книги через pgvector
          → Генерирует рекомендации
          → Сохраняет результат в Redis
      → Пользователь → GET /api/recommendations/{task_id}
          → Если готово → 200 OK с результатом
          → Если еще в работе → 202 Accepted


## 4. Стек технологий
    - Бекенд: FastAPI
    - База данных: PostgreSQL + pgvector
    - Кеш/Брокер: Redis
    - Очередь задач: Celery
    - ИИ: OpenAI Embeddings API
    - Контейнеризация: Docker + docker-compose

## 5. Структура проекта (как будут организованы файлы)
    book-recommender/
    ├── app/
    │   ├── api/
    │   │   ├── __init__.py
    │   │   ├── books.py          # Роуты для дневника
    │   │   └── recommendations.py # Роуты для рекомендаций
    │   ├── core/
    │   │   ├── __init__.py
    │   │   └── config.py         # Настройки (БД, Redis, OpenAI)
    │   ├── db/
    │   │   ├── __init__.py
    │   │   ├── session.py        # Подключение к PostgreSQL
    │   │   └── models.py         # SQLAlchemy модели
    │   ├── services/
    │   │   ├── __init__.py
    │   │   ├── book_service.py   # Логика дневника
    │   │   └── recommender.py    # Логика подбора
    │   └── tasks/
    │       ├── __init__.py
    │       └── celery_app.py     # Конфигурация Celery
    ├── tests/
    ├── docker-compose.yml
    ├── Dockerfile
    ├── requirements.txt
    └── README.md

## 6. Чему я учусь
    - Проектирование микросервисной архитектуры
    - Асинхронная обработка задач через Celery + Redis
    - Семантический поиск через pgvector и эмбеддинги OpenAI
    - Разделение на слои: router → service → repository
    - Контейнеризация приложения в Docker

## Запуск

