# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

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

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

INTRODUCTION
This Trivia API was created to play a trivia game, as part of the Full Stack Nanodegree Program designed by Udacity. The API is organized around REST. The API has resource-oriented URLs, accepts JSON request bodies, returns JSON-encoded responses, and uses standard HTTP response codes and verbs. It interacts with the database, and performs basic CRUD operations to manipulate the data.

To play, the user can retrieve the total list of questions, add a question, delete a question, or play a randomized game where the API populates a question for the user to answer. This API can easily be expanded to fit your needs.

GETTING STARTED
Base URL: Currently, this game can only be run on your local machine and not hosted as a base URL. By default, it can be run at http://127.0.0.1:5000/ or http://localhost:5000/

API Keys/Authentication: This API does not require API keys or authentication.

ERRORS
Errors:
This API uses conventional HTTP response codes to indicate the success or failure of your API request. They are returned as a JSON object with the status code and message outlining the specific error response type.

Sample JSON object error message:
{
    "error": 404, 
    "message": "resource not found", 
    "success": false
}

This API uses:
200 - OK. Your API request was successful. Everything worked as expected.
404 - Not Found. The requested resource doesn't exist, indicating an API request failure based on the information provided. 
405 - Method Not Allowed. The API request failed due to the method being incorrect for the specified endpoint.
422 - Unprocessable Request. An API request failure based on the request being unprocessable to the backend.
500 - Internal Server Error. A general error that something has gone wrong on the server.


ENDPOINT LIBRARY:
List of Endpoints:
GET '/categories'
GET '/questions'
POST '/questions'
POST '/questions/add'
DELETE '/questions/<question_id>'
GET '/categories/<category_id>/questions'
POST '/quizzes'

To perform a curl request to test these endpoints, navigate to the /backend folder in the project directory.


GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category

- Request Arguments: None
Sample cURL request:
curl http://localhost:5000/categories

- Returns: An object with a single key, categories, that contains a object of id: category_string as key:value pairs. 
Sample response body:
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true, 
  "total_categories": 6
}


GET '/questions'
- Fetches a dictionary of the total list of questions in order of ID, and results are paginated in groups of 10. 
- Request: Arguments: None
Sample cURL request:
curl http://localhost:5000/questions

- Returns: 
An array of objects, with a single key, questions, formatted as key:value pairs, of keys: answer, catagory, and difficulty, id, and question, and displays the value to the frontend.
An object with a single key, categories, that contains an object of id:category_string as key:value pairs. 
The current_category object is returned in the same format as above. 
Finally, a count of the total questions, and a success message is returned, indicating everything worked as expected.
Sample response body:
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "questions": [
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }
  ], 
  "success": true, 
  "total_questions": 22
}


POST '/questions/add'
- Post a new question to the database using form submission, requiring fields: question, answer, category and difficulty as a string. Upon submit, a new entry is created to the database with a new id, and if successful, will return a success message in the form of an alert to the frontend.

- Request: Arguments(required): Send a JSON object with key:value pairs of keys: question, answer, difficulty, and category.
Sample request body:
data: JSON.stringify({
        question: 'What author wrote "To Kill a Mockingbird\?"',
        answer: 'Harper Lee',
        difficulty: 2,
        category: 5
      })
Sample cURL request:
curl -X POST 'http://127.0.0.1:5000/questions/add' \
-H 'Content-Type: application/json' \
--data-raw '{
    "question": "What author wrote '\''To Kill a Mockingbird?'\''",
    "answer": "Harper Lee",
    "difficulty": "2",
    "category": "5"
}'

- Returns: A simple JSON object with key 'success' will be returned to indicate your request was processed as expected.
{
  "success": true
}


DELETE '/questions/<question_id>'
- Delete a question by id by hitting the trash can symbol on a given question. Question id is passed to the backend via HTTP resource URI.

- Request: Arguments: None
Sample cURL request:
curl -X DELETE http://localhost:5000/questions/29

- Returns: Returns a JSON object with the deleted question id, a success message, and the total questions count.
Sample response body:
{
  "deleted_question": 29, 
  "success": true, 
  "total_questions": 27
}


POST '/questions'
- Search questions for any phrase, not case-sensitive, can be a full or partial string.

- Request: Arguments(required): A JSON object, with the key: searchTerm.
Sample cURL request:
curl -X POST http://127.0.0.1:5000/questions \
-H 'Content-Type: application/json' \
--data-raw '{
    "searchTerm": "in"
}'

- Returns: Returns a JSON object with the category of questions retrieved, the question or questions inclusive of the searchTerm, a count of total questions returned and a success message that everything worked as expected.
Sample reponse body:
{
  "current_category": [
    "Art"
  ], 
  "questions": [
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}


GET '/categories/<category_id>/questions'
- Gets questions by category id by passing category id in HTTP URI.

- Request: Arguments: None
Sample cURL request:
curl http://127.0.0.1:5000/categories/1/questions

- Returns: Returns questions by category id of HTTP URI, category type as a string, count of total questions returned, and a success message indicating everything worked as expected.
Sample response body:
{
  "current_category": [
    "Science"
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
    }
  ], 
  "success": true, 
  "total_questions": 3
}


POST '/quizzes'
- To play game, retrieve questions based on all categories or a given category by id, and return a random question within the given category. Current question id is recorded in a list, previous_questions, and game play will retrieve next question at random.

- Request: Arguments(required): A JSON object with the list of previous questions, if applicable, and selected category by id. If ALL categories is selected, 0.
data: JSON.stringify({
    'previous_questions': [],
    'quiz_category': {'id': 0},
})
Sample cURL request:
curl -X POST 'http://127.0.0.1:5000/quizzes' \
-H 'Content-Type: application/json' \
--data-raw '{
    "previous_questions": [],
    "quiz_category": {"id":2}
}'

- Returns: Returns a JSON object containing a list of previous questions, and a random question by category id.
Sample Response Body:
{
  "previous_questions": [
    16, 
    19, 
    18
  ], 
  "question": {
    "answer": "Mona Lisa", 
    "category": 2, 
    "difficulty": 3, 
    "id": 17, 
    "question": "La Giaconda is better known as what?"
  }, 
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