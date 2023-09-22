# Company-restaurant-service-api-test

## Table of Contents
 1. [Introduction](#introduction)
 2. [Requirements](#requirements)
 3. [Installation](#installation)
 4. [Used technologies](#used-technologies)
 5. [Endpoints](#endpoints) 
 6. [Screenshots](#screenshots) 


## Introduction
Solution for test task of implementing
Company Restaurant service api.


## Requirements
### For local running
* python 3.8
* pip

### For running from docker
* Docker

## Installation
1. Clone this repository:
    ```https://github.com/Kirontiko/Company-restaurant-service-api-test.git```

2. Create .env file and define environmental variables following .env.sample
### 3. To run it locally
1. Create virtual environment and activate it:
   * Tooltip for windows:
     - ```python -m venv venv``` 
     - ```venv\Scripts\activate```
   * Tooltip for mac:
     - ```python -m venv venv```
     - ```source venv/bin/activate```

2. Install dependencies:
    - ```pip install -r requirements.txt```
3. Apply all migrations in database:
   - ```python manage.py migrate```
4. Run server
   - ```python manage.py runserver```
5. Create admin user
   - ```python manage.py createsuperuser```

### 3. To run it from docker
1. Run command:
      ```
      docker-compose up --build
      ```
### 4. App will be available at: ```127.0.0.1:8000```


## Used technologies
- Django framework
- Django Rest Framework
- PostgreSQL
- Docker

## Endpoints
    "user": "http://127.0.0.1:8000/api/user/",
    "restaurants": "http://127.0.0.1:8000/api/restaurant/restaurants/",
    "dish_types": "http://127.0.0.1:8000/api/restaurant/dish_types/",
    "dishes": "http://127.0.0.1:8000/api/restaurant/dishes/",
    "menus": "http://127.0.0.1:8000/api/restaurant/menus/",
    "votes": "http://127.0.0.1:8000/api/vote/votes/"

## Screenshots

### DB Schema

![image](https://github.com/Kirontiko/Company-restaurant-service-api-test/assets/90575903/f9293ad5-a20e-4040-91e8-08ed3ba73824)

### Restaurants

![image](https://github.com/Kirontiko/Company-restaurant-service-api-test/assets/90575903/cd5b55e4-6319-4b56-bd45-08c006a1c2c1)

### Dish Types
![image](https://github.com/Kirontiko/Company-restaurant-service-api-test/assets/90575903/63893bdc-7405-47e0-b161-d6c9e0357450)

### Dishes
![image](https://github.com/Kirontiko/Company-restaurant-service-api-test/assets/90575903/58a602ff-3340-4962-9593-a196aa0a8de1)

### Menus
![image](https://github.com/Kirontiko/Company-restaurant-service-api-test/assets/90575903/bfeea9fb-82b8-444e-88b9-7b8bb9e9c361)

### Vote for menu
![image](https://github.com/Kirontiko/Company-restaurant-service-api-test/assets/90575903/ef21dafe-f7fb-49a1-a897-8d704d1d46ac)

### Votes
![image](https://github.com/Kirontiko/Company-restaurant-service-api-test/assets/90575903/62234209-3693-4016-8a9c-dbeaf5b715f4)

### Vote Results
![image](https://github.com/Kirontiko/Company-restaurant-service-api-test/assets/90575903/1fe85300-c30b-4bc8-bf93-3338ef93c8ce)
