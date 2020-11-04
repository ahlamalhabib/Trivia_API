import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
DB_USER = os.getenv('DB_USER', 'ahlamalhabib')

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = os.getenv('DB_NAME', 'trivia_test')
        self.database_path = 'postgresql+psycopg2://{}@{}/{}'.format( DB_USER, DB_HOST, self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    
    def test_get_categories(self):
        # make request and process response
        res = self.client().get('categories')
        data = json.loads(res.data)
        # Assertions
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_error_for_requesting_non_existing_category(self):
        # make request and process response
        res = self.client().get('categories/9999')
        data = json.loads(res.data)
        # Assertions
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')  

    def test_get_questions(self):
        
        # make request and process response
        res = self.client().get('questions')
        data = json.loads(res.data)

        # Assertions
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['category'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['question'])
        self.assertEqual(len(data['question']), 10)

    
    def test_error_for_out_of_bound_page(self):
        
        # make request and process response
        res = self.client().get('questions?page=10000000')
        data = json.loads(res.data)
        # Assertions
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    
    def test_delete_question(self):
        #make request and process 
        question = Question(question='new question', answer='new answer',
                            difficulty=1, category=1)
        question.insert()
        question_id = question.id

        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)

        question = Question.query.filter(
            Question.id == question.id).one_or_none()
        # Assertions
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id)
        self.assertEqual(question, None)  

    def test_error_for_deleting_non_existing_question(self):
        #make request and process 
        question = Question(question='new question', answer='new answer',
                            difficulty=1, category=1)
        question.insert()
        question_id = question.id
        self.client().delete(f'/questions/{question_id}')
        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)
        # Assertions
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    def test_create_question(self):
        #make request and process
        new_question = {
            'question': 'new question',
            'answer': 'new answer',
            'difficulty': 1,
            'category': 1
        }
        res = self.client().post('questions', json=new_question)
        data = json.loads(res.data)
        # Assertions
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data["success"], True)
        self.assertEqual(data['message'], 'Question successfully created!')

    def test_error_for_create_question_with_empty_data(self):
        #make request and process
        request_data = {
            'question': '',
            'answer': '',
            'difficulty': 1,
            'category': '',
        }

        res = self.client().post('questions', json=request_data)
        data = json.loads(res.data)

        # Assertions
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    def test_search_questions(self):
        #make request and process
        search_question = {'searchTerm':'Whose autobiography is entitled '}
        res = self.client().post('questions/search', json= search_question)
        data= json.loads(res.data)
        # Assertions
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 1)

    def test_error_for_empty_search_term(self):
        #make request and process
        search_question = {'searchTerm': ''}

        res = self.client().post('questions/search', json=search_question)
        data = json.loads(res.data)

        # Assertions
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    def test_error_for_search_term_not_found(self):
        # make request and process response
        search_question = {'searchTerm':'What is your name' }
        res = self.client().post('questions/search', json=search_question)
        data = json.loads(res.data)

        # Assertions
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_get_questions_per_category(self):
        # make request and process response
        res = self.client().get('categories/1/questions')
        data = json.loads(res.data)
        # Assertions
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_error_for_get_questions_per_category(self):
        # make request and process response
        res = self.client().get('categories/a/questions')
        data = json.loads(res.data)
        # Assertions
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")

    def test_error_for_invalid_category_id(self):
        # make request and process response
        res = self.client().get('/categories/6780/questions')
        data = json.loads(res.data)

        # Assertions
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    def test_play_quiz_questions(self):
        """Tests playing quiz questions"""

        # mock request data
        request_data = {
            'previous_questions': [5, 9],
            'quiz_category': {
                'type': 'History',
                'id': 4
            }
        }

        # make request and process response
        response = self.client().post('/quizzes', json=request_data)
        data = json.loads(response.data)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

        # Ensures previous questions are not returned
        self.assertNotEqual(data['question']['id'], 5)
        self.assertNotEqual(data['question']['id'], 9)

        # Ensures returned question is in the correct category
        self.assertEqual(data['question']['category'], 4)

    def test_no_data_to_play_quiz(self):
        """Test for the case where no data is sent"""

        # process response from request without sending data
        response = self.client().post('/quizzes', json={})
        data = json.loads(response.data)

        # Assertions
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request error')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()