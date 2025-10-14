# DDS - Система управления движением денежных средств

Веб-сервис для учета, управления и анализа поступлений и списаний денежных средств компании или частного лица.

## 🚀 Возможности приложения

### Основной функционал
- ✅ **Создание записей о движении денежных средств**
- ✅ **Просмотр списка всех записей**
- ✅ **Редактирование и удаление** любых записей
- ✅ **Фильтрация записей**

## 🛠 Технологии

- **Backend**: Python 3.13+, Django 5.2
- **API**: Django REST Framework (DRF)
- **База данных**: SQLite (для разработки)
- **Документация**: DRF Spectacular (OpenAPI 3.0)
- **Интерфейс**: Django Admin Panel + Swagger UI
- **Autocomplete**: django-autocomplete-light
- **Фильтрация**: django-filter

## 📦 Установка и запуск

### 1. Клонирование репозитория
```bash
  git clone <url-репозитория>
```
### 2. Установка PDM и зависисмостей
```bash
  pip install pdm
  pdm install
```
### 3. Настройка базы данных
```bash
  pdm run python manage.py makemigrations
  pdm run python manage.py migrate
```
### 4. Создание суперпользователя
```bash
  pdm run python manage.py createsuperuser
```
### 5.  Загрузка начальных данных (опционально)
```bash
  pdm run python manage.py initial
```
### 5.  Запуск сервера разработки
```bash
  pdm run python manage.py runserver
```

## 📚 Использование

Django Admin Panel

Доступ: http://localhost:8000/admin/

Возможности админки:

* ✅ Полное управление всеми моделями (CRUD)
* ✅ Динамические формы с зависимыми полями (autocomplete)
* ✅ Автоматическая фильтрация подкатегорий на основе выбранной категории 
* ✅ Фильтрация и поиск по записям ДДС 
* ✅ Валидация данных на стороне сервера и клиента

REST API

Базовый URL: http://localhost:8000/dds/api/

Основные endpoints:
```http
GET /dds/api/money_movements/ - Список операций ДДС
POST /dds/api/money_movements/ - Создание новой операции
GET /dds/api/money_movements/{id}/ - Детали операции
PUT /dds/api/money_movements/{id}/ - Обновление операции
DELETE /dds/api/money_movements/{id}/ - Удаление операции
```
Справочники:

* /dds/api/statuses/ - Управление статусами
* /dds/api/operation_types/ - Управление типами операций
* /dds/api/categories/ - Управление категориями
* /dds/api/subcategories - Управление подкатегориями

Документация API

* Swagger UI: http://localhost:8000/dds/api/schema/swagger/
* ReDoc: http://localhost:8000/dds/api/schema/redoc/
* OpenAPI Schema: http://localhost:8000/dds/api/schema/