# pegb_tech
1.  git clone this project from github => https://github.com/burmese-girl/pegb_tech
2.  create virtual enviroment with the below commands if you want to separate enviromnent for this project.

    export WORKON_HOME=$HOME/virtenvs

    export PROJECT_HOME=$HOME/Projects-Active

    source $HOME/.local/bin/virtualenvwrapper.sh

    mkvirtualenv pegb_ecommerce

    After creating virtual environment, you should be on 'pegb_ecommerce' environment. If 'pegb_ecommerce' environment is not active, you can use 'workon pegb_ecommerce' command in you terminal. Now you can install dependencies with this command => pip install -r requirements.txt
  
3.  Create database with postgres, it is called 'pegb_ecommerce' because this database name already setup in settings.py inside the project folder. After creating database, you need to restore database with my "pegb_ecommerce_db.sql" then you don't need to create records in database for analysis.

Please do not use if you don't want to create data in database using "Search IP" button on Profile page.
Another options for new database but you need to search for almost all IP address in your excel because this new database will not have data for analysis.
After creating database, you need to migrate with the below command in your teminal.

        python manage.py makemigrations
        python mamage.py migrate

4.  run the server with the below command in your terminal
    python manage.py runserver

5.  You can create super user on terminal if you want.

        python manage.py createsuperuser

If you don't want to use super user for testing, please create normal user with this link => 'http://127.0.0.1:8000/user/register/'

In this step, you can give the username, email and password as you want.

6. There are login api, add_product api and discount config api in rest_framework :
    add_product api : http://127.0.0.1:8000/user/api/add_product/
    sample json format for login api from :
       **{
           "name": "pineapple",
            "selling_price": 100,
            "weight": 10,
            "quantity": 12,
            "product_category": "local fruits"
       }**

    login api : http://127.0.0.1:8000/user/api/user_login
        **{
        "username": "mayyiaung91@gmail.com",
        "password": "admin"
        }**