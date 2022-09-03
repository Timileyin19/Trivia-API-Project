import os
from unicodedata import category
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "timmytech", "", "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)
        
    

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            
        self.new_question = { 'question': 'Full meaning of WHO?', 'answer': 'World Health Organization', 'category': 1, 'difficulty': 3  }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        if (len(data['categories']) > 0): 
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['categories'])
        else: 
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertFalse(data['categories'])
            
    
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        
    def test_404_sent_requesting_beyond_valid_page(self): 
        res = self.client().get('/questions?page=5000')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_delete_question(self):
        res = self.client().delete('questions/2')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        
    def test_422_response_if_book_does_not_exist(self):
        res = self.client().delete('/questions/5000')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        
    def test_get_questions_search_with_results(self):
        res = self.client().post('/questions', json={ 'search': 'author' })
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        
    def test_get_questions_search_without_results(self):
        res = self.client().post('/questions', json={ 'search': 'lorem lipsum' })
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], 0)
        
   
    def test_add_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
    
    def test_get_questions_by_categories(self): 
        res = self.client().get('/categories/4/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
        self.assertTrue(len(data['categories']))
        
        
        
    def test_get_questions_using_category_that_does_not_exist(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
        
    def test_get_quiz_questions_successful(self):
        user_request = { 'previous_questions': [], 
                        'quiz_category': {
                            'id': 6,
                            'type': 'Sports'
                        }}
        res = self.client().post('/quizzes', json=user_request)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        
        
    def test_get_quiz_questions_with_bad_request(self): 
        res = self.client().post('/quizzes', json={})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')
        
        
    
    
        
        
        

        
        
        
        
        
    
    
        
        
        
        
            
    
    
    
    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()