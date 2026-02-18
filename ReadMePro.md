#  Распаковка проекта для разработки

> **AntiStress_shop** — инструкция по настройке локального окружения

---

## 1️⃣ Установка MongoDB

```powershell
# 1. Скачать MongoDB с сайта:
#  https://mongodb.en.softonic.com/

# 1.1 Установить MongoDB на компьютер

# 1.2 Открыть PowerShell от имени администратора

# 1.3 Перейти в папку с бинарными файлами:
cd "C:\Program Files\MongoDB\Server\8.2\bin"

# 1.4 Запустить сервер MongoDB:
mongod.exe
```

>  **Важно:** Не закрывайте это окно PowerShell — сервер должен работать постоянно.

---

## 2️⃣ Настройка PostgreSQL (pgAdmin)

```powershell
# 2.1 Открыть pgAdmin
# 2.2 Создать базу данных с именем:
```

| Параметр | Значение |
|----------|----------|
| **Имя базы данных** | `union_db` |

---

## 3️⃣ Скачивание проекта

```powershell
# 3.1 Скачать репозиторий:
#  https://github.com/fatAcake/DB_project/tree/pre_MVP

# 3.2 Распаковать архив в удобную директорию
```

---

## 4️⃣ Настройка бэкенда 

```powershell
# 4.1 Открыть PowerShell и перейти в директорию проекта
# (где находятся папки frontend и backend)

# 4.2 Создать виртуальное окружение:
python -m venv venv

# 4.3 Активировать окружение:
.\venv\Scripts\Activate.ps1

# 4.4 Установить зависимости:
pip install -r requirements.txt

# 4.5 Перейти в папку backend:
cd .\backend\

# 4.6 Создать файл .env:
new-item .env

# 4.7 Скопировать содержимое из .env.example в .env:
# (откройте файл и вставьте данные)

# 4.8 Ввести свои данные для PostgreSQL:
POSTGRES_USER=ваш_пользователь
POSTGRES_PASSWORD=ваш_пароль
POSTGRES_DB=union_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# 4.9 Запустить сервер:
uvicorn main:app --reload
```

## 5️⃣ Настройка фронтенда 

```powershell
# 5.1 Открыть НОВЫЙ PowerShell и перейти в директорию frontend:
cd путь\к\проекту\frontend

# 5.2 Установить зависимости:
npm install

# 5.3 Запустить режим разработки:
npm run dev

# 5.4 Открыть в браузере:
#  http://localhost:3000/
```

---

##  Схема рабочих процессов

```
┌─────────────────────────────────┐
│ 🔹 PowerShell #1                │
│ → mongod.exe                    │
│ → MongoDB: порт 27017           │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│ 🔹 PowerShell #2 (backend)      │
│ → uvicorn main:app --reload     │
│ → API: http://localhost:8000    │
│ → Docs: http://localhost:8000/docs
└─────────────────────────────────┘

┌─────────────────────────────────┐
│ 🔹 PowerShell #3 (frontend)     │
│ → npm run dev                   │
│ → UI: http://localhost:3000/    │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│ 🔹 pgAdmin                      │
│ → PostgreSQL: порт 5432         │
│ → БД: union_db                  │
└─────────────────────────────────┘
```

---

## ⚠️ ВАЖНО

>  **Для корректной работы проекта должны быть одновременно запущены:**
> 1. PowerShell с `mongod.exe` (MongoDB)
> 2. PowerShell с `uvicorn main:app --reload` (Backend)
> 3. PowerShell с `npm run dev` (Frontend)
> 4. pgAdmin с активной базой `union_db` (PostgreSQL)

---

##  Чек-лист запуска

- [ ] MongoDB запущен (`mongod.exe` в отдельном окне)
- [ ] База `union_db` создана в pgAdmin
- [ ] Проект скачан и распакован
- [ ] Виртуальное окружение создано и активировано
- [ ] Зависимости установлены (`pip install -r requirements.txt`)
- [ ] Файл `.env` создан и настроен
- [ ] Бэкенд запущен: `uvicorn main:app --reload`
- [ ] Фронтенд запущен: `npm run dev`
- [ ] Сайт доступен по адресу: [http://localhost:3000/](http://localhost:3000/)

---

##  Частые ошибки

| Ошибка | Решение |
|--------|---------|
| `python : Имя "python" не распознано` | Добавьте Python в PATH или используйте `py` вместо `python` |
| `Activation of virtual environment failed` | Запустите PowerShell от имени администратора или выполните `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| `ValidationError: Field required` | Проверьте, что все переменные в `.env` заполнены |
| `Port 8000/3000 already in use` | Завершите процесс, использующий порт, или измените порт в команде запуска |
