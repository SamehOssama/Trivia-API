import os
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
            'test', 'test', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            'question': 'test',
            'answer': 'test',
            'difficulty': 10,
            'category': 5
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for
    successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.get_data(as_text=True))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.get_data(as_text=True))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))
        self.assertTrue(len(data['current_category']))

    def test_404_out_of_range_page(self):
        res = self.client().get('/questions?page=10000')
        data = json.loads(res.get_data(as_text=True))

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_create_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.get_data(as_text=True))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created_id'])

    def test_delete_question(self):
        question_id = Question.query.filter(
            Question.question == 'test', Question.answer == 'test').first().id
        res = self.client().delete('/questions/{}'.format(question_id))
        data = json.loads(res.get_data(as_text=True))

        question = Question.query.filter(
            Question.question == 'test',
            Question.answer == 'test').one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], question_id)
        self.assertEqual(question, None)

    def test_422_failed_to_delete_question(self):
        res = self.client().delete('/questions/10000')
        data = json.loads(res.get_data(as_text=True))

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_search_question_with_results(self):
        search = {'searchTerm': 'title'}
        res = self.client().post('/questions/search', json=search)
        data = json.loads(res.get_data(as_text=True))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['current_category']))

    def test_search_question_without_results(self):
        search = {'searchTerm': 'testtesttesttest'}
        res = self.client().post('/questions/search', json=search)
        data = json.loads(res.get_data(as_text=True))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(len(data['current_category']), 0)

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.get_data(as_text=True))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['current_category']))

    def test_404_nonexistent_category(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.get_data(as_text=True))

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_playing_quiz_game(self):
        request = {'previous_questions': [],
                   'quiz_category': {'type': '', 'id': 3}}
        for i in range(5):
            res = self.client().post('/quizzes', json=request)
            data = json.loads(res.get_data(as_text=True))

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(len(data['previous_questions']), i)

            if not data['question']:
                break
            request['previous_questions'].append(data['question']['id'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
