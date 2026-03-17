# Task 3: System Agent – Adding query_api

## 1. Описание нового инструмента
Добавляем инструмент `query_api`, который позволяет агенту отправлять HTTP-запросы к развернутому бэкенду (LMS). Инструмент будет использовать переменные окружения `LMS_API_KEY` (для аутентификации) и `AGENT_API_BASE_URL` (базовый URL бэкенда).

## 2. Схема инструмента (function calling)
- **name**: `query_api`
- **description**: "Send an HTTP request to the backend API. Use this to get live data from the system, such as item counts, status codes, or error responses."
- **parameters**:
  - `method` (string, required): GET, POST, PUT, DELETE
  - `path` (string, required): endpoint path (e.g., "/items/")
  - `body` (string, optional): JSON body for POST/PUT

## 3. Реализация
Используем `urllib.request` из стандартной библиотеки. Добавляем заголовок `Authorization: Bearer <LMS_API_KEY>`. Возвращаем JSON с полями `status_code` и `body`. Обрабатываем HTTP-ошибки и сетевые исключения.

## 4. Обновление системного промпта
В промпте указываем, когда использовать каждый инструмент:
- `read_file` – для документации и кода.
- `list_files` – для обзора структуры.
- `query_api` – для данных от работающего сервера.
После получения результата – завершать диалог.

## 5. План итераций по бенчмарку
1. Запустить `run_eval.py`, записать начальный счёт.
2. Анализировать провалы: если не вызывается `query_api` – уточнить промпт; если неверные аргументы – улучшить описание; если ошибки API – проверить ключ и URL.
3. Повторять до прохождения всех 10 локальных вопросов.
