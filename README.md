# Hotel_Manage_System_Using_Django
This repository is a project of Object-Oriented course using Python and Django

## Feature
+ User / staff login 
+ User signup
+ Add hotel / location
+ Edit / view hotels
+ Search
+ Hotel reservation
+ Delete / view reservation detail
+ Extra facilities
+ User / staff chat
+ Customer reviews
  
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
