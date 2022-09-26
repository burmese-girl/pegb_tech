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
7. login api : http://127.0.0.1:8000/user/api/user_login
8. sample json **request** format for login api from postman or rest_framework browser:
 
         {
             "username": "mayyiaung91@gmail.com",
              "password": "admin"
         } 
9. add_product api : http://127.0.0.1:8000/user/api/add_product
10. sample json **request** format for add product api from postman or rest_framework browser:       
          
        {
              "name": "pineapple",
               "selling_price": 100,
               "weight": 10,
               "quantity": 12,
               "product_category": "local fruits"
          }
 

11. discount_config api : http://127.0.0.1:8000/user/api/discount_config  
12. sample json request format for discount_config api
       
         {
                 "name": "Silver",
                 "amount_percent": 15
          }

 
13. #For AWS Deployment in production , we should have the separated settings.py  file for cloud server configuration for S3 bucket, RDBMS and EC2 instance.

AWS_ACCESS_KEY_ID = 'your_access_key'
AWS_SECRET_ACCESS_KEY = 'your_secret_key'
AWS_STORAGE_BUCKET_NAME = 'your_s3_bucket'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'

STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# Django storages - use in production
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

#Database Setting for postgresql in AWS RDS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'your_rds_databas',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'awseb-e-dzbknmpkep-stack-awsebrdsdatabase-qbta3ehfdx05.cx2pjad2lw3a.ap-southeast-1.rds.amazonaws.com', #put your AWS rds endpoint here, this is the sample endpoint 
        'PORT': '5432',
    }
}