
# Структура проекта test_fastapi_webapp
Задание 1
Структура проекта `test_fastapi_webapp` с кратким описанием 

```plaintext
test_fastapi_webapp/
├── app/                           # Основная директория приложения
│   ├── __init__.py                
│   ├── main.py                    # Энтри поинт, запускает приложение
│   ├── dependencies.py            # Соеденение с Редисом
│   ├── models.py                  # Модель с использованием pydantic, определет структуру запросов и ответов.
│   └── routers/                   # Папка с роутам
│       ├── __init__.py            
│       └── data_router.py         # Эндпоинты(ручки) для функционала описаново в задании
├── tests/                         # Тесты с pytest
│   ├── __init__.py                
│   ├── conftest.py                # Фикстуры для тестов.
│   └── test_main.py               # Тесты для эндпоинтов FastAPI
├── poetry.lock                    # Файл блокировки,Poetry
├── pyproject.toml                 # Файл конфигурации  Poetry
├── Dockerfile                     # Инструкции для Докера по сборке образа приложения
└── docker-compose.yml             # Определяет сервисы, собираем приложение и редис вместе


# Задание 2

## Варианты обновления данных из таблицы `short_names` в `full_names`

### 1) Обновление с использованием подзапроса

```sql
UPDATE full_names
SET status = (
    SELECT status
    FROM short_names
    WHERE name = split_part(full_names.name, '.', 1)
)
WHERE EXISTS (
    SELECT 1
    FROM short_names
    WHERE name = split_part(full_names.name, '.', 1)
);

### 2) Вариант обновление через JOIN

```sql
UPDATE full_names
SET status = short_names.status
FROM short_names
WHERE short_names.name = split_part(full_names.name, '.', 1);


### 3) Вариант  использование временной таблицы 
-- Создаем временную таблицу
CREATE TEMP TABLE temp_update AS
SELECT split_part(f.name, '.', 1) as short_name, s.status
FROM full_names f
JOIN short_names s ON s.name = split_part(f.name, '.', 1);

-- Индекс временной таблицы для ускорения JOIN
CREATE INDEX ON temp_update (short_name);

-- Обновление основной таблицы используя временную
UPDATE full_names f
SET status = t.status
FROM temp_update t
WHERE split_part(f.name, '.', 1) = t.short_name;

-- Удаление временной таблицы 
DROP TABLE temp_update;
