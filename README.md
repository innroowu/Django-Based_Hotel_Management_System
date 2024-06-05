# Django-Based Hotel Management System
This repository is a project of Object-Oriented course using Python and Django

## Feature
+ User / staff login or signup
+ Edit / view hotels
+ Add hotel / location
+ Search 
+ Hotel reservation
+ Delete / view reservation detail
+ Customer reviews
+ Extra facilities
+ User / staff contact system
+ Sales historical analysis

## File Organization
```
Hotel_Management_System\hotel
    ├─ hotel/
       ├─ asgi: ASGI config for hotel project
       ├─ settings: Django settings for hotel project
       ├─ urls: hotel URL Configuration
       └─ wsgi: WSGI config for hotel project.
    ├─ management/
       ├─ migration: all the migration files inside here
       ├─ static: icon and bootstrap
       ├─ templatetags: 
       ├─ admin: ASGI config for hotel project
       ├─ apps: django apps config
       ├─ models: Our models class
       ├─ tests: nothing
       └─ views: receives requests and returns responses
    ├─ templates/..: The html files of our entire system are in this folder
    ├─ manage: Just follow the instructions below to execute this file
    └─ create_booking: Used to create booking database
```

## Setup
1. Clone the repository
   
2. Install Django

3. Database migration
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```
4. Run server
    ```
    python manage.py runserver 127.0.0.1:8000
    ```

5. After execution, if the database has not created the corresponding table ( eg. no such table: room_room )
   
   (OPTIONAL) Check which migration files have been applied  
    ```
    python manage.py showmigrations
    ```
   Make sure there is a valid model definition in the application in model.py. Then, create a new migration file.
    ```
    # python manage.py makemigrations <model_name>
    python manage.py makemigrations room
    python manage.py migrate
    ```
    Execute run server again
    
    
## Configuration
+ Make sure the 'STATIC_URL' in <setting.py> points to the valid directory containing your static files, such as images, CSS stylesheets, JavaScript files, etc.

+ DATABASES in <setting.py> must also direct to the correct db.sqlite3 file
