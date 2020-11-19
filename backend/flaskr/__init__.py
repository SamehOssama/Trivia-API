import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    def paginate_questions(request, selection):
        """
        Paginate the data and formats it depending on the page number.
        Attributes:
        request: the request data sent by the browser.
        selection: the database values that we want to paginate.
        """
        page = request.args.get('page', 1, type=int)
        start = (page-1)*QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        formatted_questions = [question.format() for question in selection]
        current_questions = formatted_questions[start:end]

        return current_questions

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
        """
        Get the all the categories as an array [id:"category_name"].
        """
        categories = Category.query.order_by(Category.id).all()
        formatted_categories = {
            category.id: category.type for category in categories}

        return jsonify({
            'success': True,
            'categories': formatted_categories
        })

    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom
    of the screen for  three pages.
    Clicking on the page numbers should update the questions.
    '''
    @app.route('/questions', methods=['GET'])
    def get_questions():
        """
        Get the all the questions and categories as a dictionary
        """
        categories = Category.query.all()
        formatted_categories = {
            category.id: category.type for category in categories}
        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, questions)
        current_category = [category['category']
                            for category in current_questions]
        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions),
            'categories': formatted_categories,
            'current_category': current_category
        })

    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.
    TEST: When you click the trash icon next to a question,
    the question will  be removed.
    This removal will persist in the database and when you refresh the page.
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """
        Delete a question by its ID.
        """
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()
            question.delete()
            return jsonify({
              'success': True,
              'deleted_id': question_id
            })
        except:
            abort(422)

    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.
    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will
    appear at the end of the last page
    of the questions list in the "List" tab.
    '''
    @app.route('/questions', methods=['POST'])
    def create_question():
        """
        Create a new question.
        """
        # try:
        data = request.get_json()
        question = Question(
            question=data.get('question'),
            answer=data.get('answer'),
            category=data.get('category'),
            difficulty=data.get('difficulty')
        )
        question.insert()

        return jsonify({
            'success': True,
            'created_id': question.id
        })
        # except:
        #     abort(422)

    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.
    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        """
        Get all the questions that contains a term equal to
        the search term from the post request.
        The search is case insensitive.
        """
        results = Question.query.filter(Question.question.ilike(
            f"%{request.json.get('searchTerm')}%")).order_by(Question.id).all()
        current_questions = paginate_questions(request, results)
        current_category = [category['category']
                            for category in current_questions]
        return jsonify({
            'success': True,
            'questions': current_questions,
            'current_category': current_category,
            'total_questions': len(results)
          })

    '''
    @TODO:
    Create a GET endpoint to get questions based on category.
    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_category_questions(category_id):
        """
        Get all the questions with the specified category ID
        """
        category = Category.query.filter(
            Category.id == category_id).one_or_none()
        if category is None:
            abort(404)
        questions = Question.query.filter(
            Question.category == category_id).order_by(Question.id).all()
        current_questions = paginate_questions(request, questions)
        current_category = [category['category']
                            for category in current_questions]

        return jsonify({
            'success': True,
            'questions': current_questions,
            'current_category': current_category,
            'total_questions': len(questions)
        })

    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''
    @app.route('/quizzes', methods=['POST'])
    def play():
        """
        Get one question per request while ignoring the questions already used.
        Questions can be specified by category or all categories (ID = 0)
        """
        category_id = request.get_json()['quiz_category']['id']
        previous_questions = request.get_json()['previous_questions']

        if category_id == 0:
            question = Question.query.filter(
                Question.id.notin_(previous_questions)).first()
        else:
            question = Question.query.filter(
                Question.category == category_id,
                Question.id.notin_(previous_questions)).first()

        if question is None:
            # End the quizz game if the database can't return more questions.
            formatted_question = False
        else:
            formatted_question = question.format()

        return jsonify({
            'success': True,
            'question': formatted_question,
            'previous_questions': previous_questions
          })

    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    return app
