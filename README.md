# REST APIs for a blog

## Requirement
Python 3.5+  
Flask   
MySQL  
Mysql-connector-python   
Postman Agent for API Tests

## Installation
Download Python 3.5 or newer version: https://www.python.org/downloads/  
Download MySQL server and workbench:  https://dev.mysql.com/downloads/installer/  
Install Postman Desktop Client: https://www.postman.com/downloads/  
Install Flask and mysql-connector-python using pip:  ``` pip install flask mysql-connector-python ```  

## Usage 
- Open MySQL Workbench and create database and tables using ```tables.sql``` script  
- Change database connection configuration if necessary to match your MySQL server's configuration in ```api/database/config.ini```  
- Navigate to ```api``` directory and open up the command line to start the application using ```python app.py```   
- Open Postman Client and start testing the APIs with the root url ```http://127.0.0.1:5000/```

## Endpoints 
You can test the API with the following endpoints:  
**Note: For requests with body containing data, data must be in JSON format. For requests modifying and creating data, fields in request's body must match fields in corresponding table in database**
### User endpoints
Method  | Endpoint  | Additional parameters | Description
-----   | --------  |------------------     | -----------
GET | http://127.0.0.1:5000/users | name, occupation | Get all users' information 
GET | http://127.0.0.1:5000/users/{id} | None | Get user information with given id
GET | http://127.0.0.1:5000/users/{id}/posts | None | Get user's posts with given id
POST | http://127.0.0.1:5000/users | None | Create a new user 
PUT | http://127.0.0.1:5000/users/{id} | None | Update user information with given id
DELETE | http://127.0.0.1:5000/users/{id} | None | Delete a user with given id 

### Post endpoints 
Method  | Endpoint  | Additional parameters | Description
-----   | --------  |------------------     | -----------
GET | http://127.0.0.1:5000/posts | per_page | Get all posts by all users 
GET | http://127.0.0.1:5000/posts/{id} | None | Get a post with given id 
POST | http://127.0.0.1:5000/posts | None | Create a new post 
PUT | http://127.0.0.1:5000/posts/{id} | None | Update a post with given id 
DELETE | http://127.0.0.1:5000/posts/{id} | None | Delete a post with given id

## Like endpoints 
Method  | Endpoint  | Additional parameters | Description
-----   | --------  |------------------     | -----------
GET   | http://127.0.0.1:5000/likes | user_id, post_id | Get all likes of all posts. If user_id provided, get all the posts like by that user, if post_id provided, get all likes of a post  
POST | http://127.0.0.1:5000/likes | None | Create a new like when a user likes a post 
DELETE | http://127.0.0.1:5000/likes | None | Remove like when a user unlikes a post
