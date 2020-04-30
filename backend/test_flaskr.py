import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from flaskr.models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
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

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        """Test get all categories"""
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['categories']))

    def test_post_categories(self):
        """Test post request to /categories"""
        res = self.client().post('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['message'], 'method not allowed')


    def test_get_questions(self):
        """Test get request to /questions"""
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_404_fail_beyond_paginated_result(self):
        """Test paginated result of questions"""
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_paginate_questions(self):
        """Test paginated result of questions"""
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))

    # def test_delete_question(self):
    #     """ Test delete question to /questions"""
    #     res = self.client().delete('/questions/6')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['deleted_question'], 6)
    #     self.assertTrue(data['total_questions'])


    def test_fail_delete_question_beyond_index(self):
        """Test 404 if DB Questions returns None"""
        res = self.client().delete('/questions/10000')
        data = json.loads(res.data) 

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    # def test_add_new_question(self):
    #     """Test add new question to DB"""
    #     res = self.client().post('/questions/add', json={'question': 'What\'s Tuckers favorite snack?', 'answer': 'Liver bites', 'difficulty': 1, 'category': 6})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)

    def test_if_request_get_json_is_none(self):
        """Test if data is incomplete from request.get_json"""
        res = self.client().post('/questions/add', json={'question': '', 'answer': 'Liver bites', 'difficulty': 1, 'category': 6})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], 'unprocessable request')

    def test_wrong_method_add_question(self):
        """Test add new question to DB"""
        res = self.client().get('/questions/add', json={'question': 'What\'s Tuckers favorite snack?', 'answer': 'Liver bites', 'difficulty': 1, 'category': 6})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    def test_search_term(self):
        """Test search term"""
        res = self.client().post('/questions', json={'searchTerm': 'a'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['current_category'])
    

    def test_blank_search_term(self):
        """Test search term"""
        res = self.client().post('/questions', json={'searchTerm': ''})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_get_by_category(self):
        """Test retrieve questions by category"""
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['current_category'])

    def test_error_on_category_beyond_index(self):
        """Test fail on wrong category"""
        res = self.client().get('/categories/10/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_play_game(self):
        """Test play game by all categories"""
        res = self.client().post('/quizzes', json={'quiz_category':{'id': 0, 'type': 'click'}, 'previous_questions': []})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_play_game_no_current_question(self):
        """Test play game with no current question"""
        res = self.client().post('/quizzes', json={'quiz_category':{'id': 6, 'type': 'Sports'}, 'previous_questions': [10,11]})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_error_play_game_wrong_category(self):
        """Test play game with non-existent category id"""
        res = self.client().post('/quizzes', json={'quiz_category':{'id': 7, 'type': 'Music'}, 'previous_questions': {}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_server_error(self):
        """Test 500 error on internal server error"""
        res = self.client().get('/error')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'internal server error')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()