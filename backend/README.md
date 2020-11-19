# Full Stack Trivia API Backend

This project is a trivia api for udacity's advance web development nanodegree and serves as a test for our knowledge about APIs from Module 2 : API Development and Documentation. The user can access a database full of questions and their answes, can create new questions and delete whichever they want.A search option is also availble for quick access to specific questions and there is a trivia game which tests the user's knowledge about the different categories available.


- [Getting Started](#getting-started)
  - [Installing Dependencies](#installing-dependencies)
  - [Database Setup](#database-setup)
  - [Running the server](#running-the-server)
- [API References](#api-references)
  - [Errors](#errors)
  - [Endpoints](#endpoints)
  - [`GET` '/categories'](#get-categories)
  - [`GET` '/questions'](#get-questions)
  - [`GET` '/categories/category_id/questions'](#get-categoriescategory_idquestions)
  - [`POST` '/questions'](#post-questions)
  - [`POST` '/questions/search'](#post-questionssearch)
  - [`POST` '/quizzes'](#post-quizzes)
  - [`DELETE` '/questions/question_id'](#delete-questionsquestion_id)
- [Testing](#testing)


## Getting Started

---

### Installing Dependencies

#### Python 3.8

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server on windows cmd, execute:
```bash
flask_run.bat
```
Or, if using bash, execute:
```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 
## API References

----

- Base url: This app is not hosted on a web server, instead, it is hosted locally at the default ```http://127.0.0.1:5000/```
- Authentication: This version of the app doesn't require authentication.

### Errors
HTTP requests always come with a code to determine the response state from `2xx` codes that means success to `4xx` codes that means there was an error with the request.
Here is a list of the expected response codes from this API and their meaning:

| Code    | Text               | Description                                                                       |
| ------- | ------------------ | --------------------------------------------------------------------------------- |
| **200** | OK                 | Everything worked as expected.                                                    |
| **404** | Not found          | The requested resource could not be found.                                        |
| **405** | Method not allowed | The request method is not supported for the requested resource.                   |
| **422** | unprocessable      | The request was well-formed but was unable to be followed due to semantic errors. |

### Endpoints
```html
GET '/categories'
GET '/questions'
GET '/categories/category_id/questions'
POST '/questions'
POST '/questions/search'
POST '/quizzes'
DELETE '/questions/question_id'
```
### `GET` '/categories'
```bash
curl -X GET\
-H "Accept: application/json"\
"http://localhost:5000/categories"
```
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category.
- Request Arguments: None
- Returns: 
  - An object with a single key, categories, that contains an object of id: category_string key:value pairs.
#### Response Body:
```json
{
"categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
},
"success": true
}
```

### `GET` '/questions'
```bash
curl -X GET \
-H "Accept: application/json" \
"http://localhost:5000/questions"
```
- Fetches a dictionary of questions in which the keys are the question's information and the value is the corresponding data of the question.
- Request Arguments: None
- Returns: 
  - An object with multiple keys
    - categories, that contains an object of id: category_string key:value pairs.
    - current categories, that contains an array of every question's category id.
    - questions, that contains an object of question_info: question_data key:value pairs.
    - total_questions, an integer that sepecifies the number of questions retireved.
#### Response Body:
```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": [
        5,
        5,
        4,
        5,
        4,
        6,
        6,
        4,
        3,
        3
    ],
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        }
    ],
    "success": true,
    "total_questions": 23
}
```

### `GET` '/categories/category_id/questions'
```bash
curl -X GET \
-H "Accept: application/json" \
"http://localhost:5000/categories/1/questions"
```
- Fetches a dictionary of questions with the specified `category_id` in which the keys are the question's information and the value is the corresponding data of the question.
- Request Arguments: None
- Returns:
  - An object with multiple keys:
    - current categories, that contains an array of every question's category id.
    - questions, that contains an object of question_info: question_data key:value pairs.
    - total_questions, an integer that sepecifies the number of questions retireved.
#### Response Body:
```json
{
    "current_category": [
        1,
        1,
        1,
        1,
        1
    ],
    "questions": [
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        },
        {
            "answer": "World",
            "category": 1,
            "difficulty": 1,
            "id": 28,
            "question": "Hello?"
        },
        {
            "answer": "World",
            "category": 1,
            "difficulty": 1,
            "id": 29,
            "question": "Hello?"
        }
    ],
    "success": true,
    "total_questions": 5
}
```

### `POST` '/questions'
```bash
curl -X POST \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
"http://localhost:5000/questions" \
-d '{"question": "Hello?", "answer": "World", "difficulty": 1, "category": 1}
```
- Sends a dictionary of question in which the keys are the question's information and the value is the corresponding data of the question.
- Request Arguments:
  - A JSON object containing the question_info: question_data in a key:value each.
- Returns: 
  - An object with a single key, created_id, and value of the created question's id in a key:value pair.
#### Request Body:
```json
{
    "question": "Hello?",
    "answer": "World",
    "difficulty": 1,
    "category": 1
}
```
#### Response Body:
```json
{
  "created_id": 30,
  "success": true
}
```

### `POST` '/questions/search'
```bash
curl -X POST \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
"http://localhost:5000/questions/search" \
-d '{"searchTerm": "title"}
```
- Send a dictionary where the key is search term and the value is the query.
- Request Arguments:
  - A JSON object containing the search term and query in a key:value pair.
- Returns: 
  - An object with multiple keys
    - current categories, that contains an array of every question's category id.
    - questions, that contains an object of question_info: question_data key:value pair each.
    - total_questions, an integer that sepecifies the number of questions retireved.
#### Request Body:
```json
{
  "searchTerm": "title"
}
```
#### Response Body:
```json
{
    "current_category": [
        4,
        5
    ],
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        }
    ],
    "success": true,
    "total_questions": 2
}
```

### `POST` '/quizzes'
```bash
curl -X POST -H "Accept: application/json" \
-H "Content-Type: application/json" \
"localhost:5000/quizzes" \
-d '{"previous_questions": [8], "quiz_category": {"id": 0}}'
```
- Fetches a dictionary with keys previous questions with a value of array of ids and the quiz category with a value of dictionary containing the quiz id and type.
    >The quiz_cateory type key:value pair is optional.
- Request Arguments: 
    - A JSON object containing: 
      - previous questions and the array of question ids in a key:value pair.
      - quiz category which is an object containing the category id and type each in a key:value pair.
- Returns: 
  - A JSON object containing: 
    - previous questions, that contains an array of question ids in a key:value pair.
    - question, that contains an object of question_info: question_data in a key:value pair each.
#### Request Body:
```json
{
    "previous_questions": [8],
    "quiz_category": {
        "id": 0,
        "type": "click"
    }
}
```
#### Response Body:
```json
{
    "previous_questions": [
        8
    ],
    "question": {
        "answer": "Maya Angelou",
        "category": 4,
        "difficulty": 2,
        "id": 5,
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    "success": true
}
```

### `DELETE` '/questions/question_id'
```bash
curl -X DELETE\
-H "Accept: application/json"\
"http://localhost:5000/questions/31"
```
- Delete a question with the specified `question_id`.
- Request Arguments: None
- Returns: 
  - An object with a single key, deleted_id, and value of the deleted question's id in a key:value pair.
#### Response Body:
```json
{
    "deleted_id": 31,
    "success": true
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```