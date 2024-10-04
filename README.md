## Quickstart for pycharm

Запуск через Docker:

    git clone https://github.com/Pezdabolius/TestCat.git
    cd TestCat 
    docker compose up --build
    docker compose exec django pytest cat/tests.py --ds=core.settings
    
## На сайт
Переходим по адресу http://localhost:8000/

swagger: http://localhost:8000/api/swagger/

django-admin: http://localhost:8000/admin/ (username=admin, password=defender)
