# 📚 Personal Library API

REST API для управления личной библиотекой пользователя.

## 👨‍💻 HR-шпаргалка (только браузер)

HR может проверить проект без командной строки:

Открой браузер по ссылке:

Главная страница библиотеки: https://my-library-unuo.onrender.com/library/main/✅  

Swagger (опционально, для разработчика): https://my-library-unuo.onrender.com/swagger/️ (прочтите замечание ниже) 

⚠️ Замечание: иногда форма для POST/PUT запросов при первом нажатии Try it out может не отображаться. Чтобы обойти, сверните и разверните запрос повторно.

Проект позволяет:  

- 📖 Создавать и редактировать книги  
- ✅ Отмечать книги как прочитанные  
- 📝 Добавлять заметки к книгам  
- 🔐 Работать через JWT-аутентификацию  
- 📑 Тестировать API через Swagger  
- 🧩 Имеется пагинация на API для списков книг  

---

## 🚀 Технологии

- Python 3.10+  
- Django 5.2.9  
- Django REST Framework 3.16.1  
- JWT — `djangorestframework_simplejwt`  
- Swagger — `drf-yasg`  
- PostgreSql  
- Pytest  
- Docker  

---

## 🖥 Как открыть командную строку

### Windows

**CMD (Command Prompt)**  
1. Нажми `Win + R` → введите `cmd` → Enter  

**PowerShell / Windows Terminal**  
1. Нажми `Win + X` → выбери `Windows PowerShell` или `Windows Terminal`

### Mac / Linux

1. Найди и открой приложение `Terminal` (Терминал)  

---

## 📂 Создание папки и переход в неё

### Windows (CMD / PowerShell)

```bat
:: Создать папку
mkdir test_hr_run

:: Перейти в папку
cd test_hr_run
Linux / MacOS (Terminal)
# Создать папку
mkdir test_hr_run

# Перейти в папку
cd test_hr_run

💡 После этого можно клонировать репозиторий и запускать проект.

⚙️ Запуск проекта

🔹 Через Docker (рекомендуется)

# Клонируем репозиторий
git clone https://github.com/the-Hodor/my_library.git

# Переходим в папку проекта
cd my_library

# Запускаем контейнеры
docker compose up --build

# Применяем миграции
docker compose exec web python manage.py migrate

# Создаём суперпользователя
docker compose exec web python manage.py createsuperuser

Сервер будет доступен по адресу:

Главная страница: http://127.0.0.1:8000/library/main/

Swagger документация: http://127.0.0.1:8000/swagger/

🔹 Локальный запуск (без Docker)

python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install --upgrade pip wheel
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

📖 Swagger документация (для разработчиков)

Через Swagger можно:

Просматривать все endpoints

Отправлять запросы

Тестировать API без Postman

⚠️ Замечание: иногда форма для POST/PUT запросов при первом нажатии Try it out может не отображаться. Чтобы обойти, сверните и разверните запрос повторно.

🔐 JWT-аутентификация

(Для разработчиков, не обязательна для HR)

Получение токена: POST /api/token/

{
  "username": "your_username",
  "password": "your_password"
}

Обновление токена: POST /api/token/refresh/

Использование: добавить заголовок

Authorization: Bearer <access_token>
📚 API Endpoints

(Для разработчиков, не обязательна для HR)

/api/books/ — CRUD для книг, с пагинацией (по 10 элементов на страницу)

/api/mark_read/<int:pk>/ — отметить книгу как прочитанную

/api/create_notes/ — создать заметку

🧪 Тестирование
pytest

Тестируется сервисный слой: book_service и note_service.

🧠 Архитектура проекта

Models Layer: Book, Genre, Note, MyUser

Service Layer: book_service.py, note_service.py — здесь живёт бизнес-логика

API Layer: DRF views, Serializers, JWT

🐳 Docker

Django backend

SQLite база данных

