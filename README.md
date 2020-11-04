
# Trivia API Project : 

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out. 

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category.


## Getting started :

pre-requisites and local Development 
Developers using this project should already have python3, pip and node installed on thier local machines .

## Backend 
From the backend folder run 
```bash
pip install -r requirements.txt
```
### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```
psql trivia < trivia.psql
```
### Running the server
To run application run the following command :

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

### Test
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## Frontend 

From Frontend folder run the following command :

```bash
npm install
```
By defulat, the frond end will run on localhost:3000


## API Reference

### Getting started 

Base URL : at present that this app can only be run localy and is not hosted as base URL. 
- Backend app is hosted at: [http://127.0.0.1:5000/]
- Frontend app is hosted at: [http://127.0.0.1:3000/]
- Authentication: This version of this application does not require Authentication or API Keys.



### Error Handling 

Errors are returned in the following json format:
```
 {
        "success": "False",
        "error": 422,
        "message": "Unprocessable entity",
      }
```
The API will return Three type of error when requesting fails :
- 400 – bad request
- 404 – resource not found
- 422 – unprocessable



### Endpoint

#### GET /categories
- General:
Returns all the categories.

- Sample: curl http://127.0.0.1:5000/categories
```
{
  "categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }, 
    {
      "id": 3, 
      "type": "Geography"
    }, 
    {
      "id": 4, 
      "type": "History"
    }, 
    {
      "id": 5, 
      "type": "Entertainment"
    }, 
    {
      "id": 6, 
      "type": "Sports"
    }
  ], 
  "success": true
}
```

#### GET /questions
- General:
Returns all questions
questions are in a paginated.
pages could be requested by a query string

- Sample: curl http://127.0.0.1:5000/questions
```
{
  "category": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "question": [
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
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 19
}
```
#### DELETE /questions/int:id\
- General:
Deletes a question by id form the url parameter.

- sample: curl -X DELETE  http://127.0.0.1:5000/questions/9
```
{
  "deleted": 9, 
  "success": true
}

POST /questions
General:
Creates a new question based on a payload.

Sample:
curl  -X POST -H "Content-Type: application/json" -d '{ "question": "Which is the only team to play in every soccer World Cup tournament?", "answer": "Brazil", "difficulty": 3, "category": "6" }' http://127.0.0.1:5000/questions 

{
  "message": "Question successfully created!", 
  "success": true, 
  "total_questions": 20
}
```

#### POST /questions/search
- General:
returns questions that has the search substring
- Sample:
curl  -X POST -H "Content-Type: application/json" -d '{"searchTerm": "The Taj Mahal"}' http://127.0.0.1:5000/questions/search 
```
{
  "questions": [
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 20
}
```
#### GET /categories/int:id\/questions
- General:
Gets questions by category using the id from the url parameter.
- Sample:
curl http://127.0.0.1:5000/categories/3/questions
```
{
  "current_category": "Geography", 
  "questions": [
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 2
}
```
#### POST /quizzes
- General
Takes the category and previous questions in the request.
Return random question not in previous questions.
- Sample: 
curl -X POST -H "Content-Type: application/json" -d '{"previous_questions": [5, 9], "quiz_category": {"type": "Geography", "id": "3"}}' http://127.0.0.1:5000/quizzes
```
{
  "question": {
    "answer": "Agra", 
    "category": 3, 
    "difficulty": 2, 
    "id": 15, 
    "question": "The Taj Mahal is located in which Indian city?"
  }, 
  "success": true
}
```

## Authros 
- Udacity provided the starter files for the project including the frontend
- Ahlam Alhabib worked on  the API.
## Acknowledgements 
The team of Udacity and my helpfull Colleagues.