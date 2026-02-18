# Разспаковка проекта для разработки 
## 1. Скачать mongoDB с сайта https://mongodb.en.softonic.com/
1.1 Установить к себе на компьютер 
1.2 Открыть PowerShell от имени администратора 
1.3 ввести cd "C:\Program Files\MongoDB\Server\8.2\bin" с кавычками
1.4 ввести mongod.exe
## 2. Открыть pgAdmin 
2.1 создать базу данных union_db
## 3. Скачать репозиторий https://github.com/fatAcake/DB_project/tree/pre_MVP
3.1 Распаковать архив куда-нибудь
## 4. Бэкенд- открыть PowerShell перейти в директорию с проектом где находятся папки frontend и backend
4.1 выполнить команду pythin -m venv venv 
4.2 выполнить команду pip install -r requirements.txt
4.3 выполнить команду cd .\backend\
4.4 создать файл .env 
4.5 скопировать содержимое из .env example
4.6 ввести свои данные в полях для postgress
4.7 выполнить команду uvicorn main:app --reload
## 5.  открыть PowerShell перейти в директорию frontend 
5.1 выполнить команду npm install 
5.2 выполнить команду npm run dev
5.3 перейдите по ссылке http://localhost:3000/

ВАЖНО для корректной работы должны быть запущены три PowerShell и pgAdmin
