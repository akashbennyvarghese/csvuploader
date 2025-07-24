# csvuploader

pip install -r requirements.txt

django-admin startproject csvuploader

cd csvuploader

python manage.py startapp api

python manage.py makemigrations

python manage.py migrate

python manage.py runserver

http://127.0.0.1:8000/swagger


# Sources

https://joel-hanson.medium.com/drf-how-to-make-a-simple-file-upload-api-using-viewsets-1b1e65ed65ca

https://medium.com/@ukemeboswilson/creating-swagger-documentation-in-django-rest-framework-a-guide-to-drf-yasg-and-drf-spectacular-216fc41d47de

https://dev.to/frankezenwanne/how-to-upload-a-csv-file-to-django-rest-28fo

https://www.django-rest-framework.org/#quickstart
