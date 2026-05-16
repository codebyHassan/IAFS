@echo off
call venv\Scripts\activate
start chrome http://127.0.0.1:3000/
python manage.py runserver 3000