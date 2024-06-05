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

## Here is the setup on web application (You can find setup on mobile web browser at the bottom) 
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
    
    
## Setup on mobile web browser: How to use ngrok to expose local servers to the internet
+ First, make sure you've installed ngrok.

+ Then, run server in your terminal.
   ```
    python manage.py runserver
    ```
   
+ At the same time, run ngrok through this command.
   ```
    ngrok http 8000
    ```
   
+ You need to copy the link after forwarding. 
   ```
   # For example, "https://6b51-118-232-108-58.ngrok-free.app" in this case
   ngrok                                                           (Ctrl+C to quit)
                                                                                
   New guides https://ngrok.com/docs/guides/site-to-site-apis/                     
                                                                                
   Session Status             online                                            
   Account                       Tsaiiiii (Plan: Free)                             
   Version                        3.10.0                                            
   Region                         Japan (jp)                                        
   Latency                        46ms                                              
   Web Interface               http://127.0.0.1:4040                             
   Forwarding                   https://6b51-118-232-108-58.ngrok-free.app -> http

   Connections                 ttl     opn     rt1     rt5     p50     p90       
                                1       0       0.00    0.00    90.39   90.39
    ```
   
+ Next, you need to paste this link in settings.py file.
   ```
   # You need to paste your unique link since ngrok will randomly generate links.
   CSRF_TRUSTED_ORIGINS = ['https://6b51-118-232-108-58.ngrok-free.app']
   ```
   
+ Finally, you can access this website through this link. You can try to use it with your mobile devices. 
