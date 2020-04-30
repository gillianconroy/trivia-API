import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from .models import *
from werkzeug.debug import console

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_qs = questions[start:end]

  return current_qs


def create_app(test_config=None):
  # Create and configure the app
  app = Flask(__name__)
  setup_db(app)
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  '''
  @DONE:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def retrieve_categories():
    categories = Category.query.all()
    catgs = {cat.id: cat.type for cat in categories}

    # Return error if query returned no categories
    if len(categories) == 0:
      abort(404)

    return jsonify({
      'categories': catgs,
      'success': True,
      'total_categories': len(categories)
    })

  '''
  @DONE:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of
  the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''
  @app.route('/questions', methods=['GET'])
  def get_questions():
    selection = Question.query.order_by(Question.id).all()
    current_qs = paginate_questions(request, selection)

    categories = Category.query.all()
    all_catgs = {cat.id: cat.type for cat in categories}

    if len(current_qs) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': current_qs,
      'total_questions': len(selection),
      'categories': all_catgs
    })

  '''
  @DONE:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question,
  the question will be removed. This removal will persist in
  the database and when you refresh the page.
  '''
  @app.route('/questions/<question_id>', methods=['DELETE'])
  def delete_question(question_id):
    delete_q = Question.query.filter_by(id=question_id).one_or_none()

    if delete_q is None:
      abort(404)

    delete_q.delete()

    return jsonify({
      'success': True,
      'deleted_question': delete_q.id,
      'total_questions': Question.query.count()
    })

  '''
  @DONE:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at
  the end of the last page of the questions list in the
  "List" tab.
  '''
  @app.route('/questions/add', methods=['POST'])
  def add_question():
    question = request.get_json()['question']
    answer = request.get_json()['answer']
    difficulty = request.get_json()['difficulty']
    category = request.get_json()['category']

    new_q = Question(question, answer, category, difficulty)

    q = {
      'question': question, 
      'answer': answer, 
      'category': category,
      'difficulty': difficulty
      }

    # Check with a simple validatation
    if all(q.values()):
      new_q.insert()
    else:
      abort(422)

    return jsonify({
      'success': True,
      'new_question': q
    })

  '''
  @DONE:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''
  @app.route('/questions', methods=['POST'])
  def search():
    search_term = request.get_json()['searchTerm']

    if search_term == '':
      abort(404)
    else:
      # Query the DB for searchTerm in substring (not case-sensitive)
      selection = Question.query.filter(
                  Question.question.ilike(f'%{search_term}%')).all()
      result = paginate_questions(request, selection)

      current_catgs = []

      # Append category type string to current_catgs.
      for r in selection:
        cat = Category.query.filter_by(id=r.category).one_or_none()
        if cat.type not in current_catgs:
          current_catgs.append(cat.type)

    return jsonify({
      'success': True,
      'questions': result,
      'total_questions': len(selection),
      'current_category': current_catgs
    })

  '''
  @DONE:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
  @app.route('/categories/<category_id>/questions', methods=['GET'])
  def get_by_category(category_id):
    selection = Question.query.filter_by(category=category_id).all()
    result = paginate_questions(request, selection)
    count_catgs = Category.query.count()

    # Check if URL resource category_id is in range of Category count
    if int(category_id) not in range(1, count_catgs + 1):
      abort(404)

    current_catgs = []
    for r in selection:
      cat = Category.query.filter_by(id=r.category).one_or_none()
      if cat.type not in current_catgs:
        current_catgs.append(cat.type)

    return jsonify({
      'success': True,
      'questions': result,
      'total_questions': len(selection),
      'current_category': current_catgs
    })

  '''
  @DONE:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''
  @app.route('/quizzes', methods=['POST'])
  def get_next_question():
    previous_q = request.get_json()['previous_questions']
    quiz_cat = request.get_json()['quiz_category']

    if quiz_cat is None:
      abort(404)

    cat_id = quiz_cat['id']

    # If all categories are selected, cat_id key "id": 0.
    if cat_id == 0:
      selection = Question.query.all()
    else:
      selection = Question.query.filter_by(category=cat_id).all()
      if int(cat_id) > 6:
        abort(404)
    questions = [question.format() for question in selection]

    # Return JSON body with no current_q if specified rounds of game play 
    # exceeds the number of questions.
    if len(previous_q) + 1 > len(questions):
      return jsonify({
        'success': True,
        'previous_questions': previous_q
      })
    else:
      current_q = random.choice(questions)
      while current_q['id'] in previous_q:
        current_q = random.choice(questions)

    return jsonify({
      # 'quiz_category': cat_id,
      'success': True,
      'previous_questions': previous_q,
      'question': current_q
    })

  @app.route('/error', methods=['GET'])
  def error_handler():
    abort(500)

  '''
  @DONE:
  Create error handlers for all expected errors
  including 404 and 422.
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "message": "resource not found",
      "error": 404,
      }), 404

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      "success": False,
      "message": "method not allowed",
      "error": 405
      }), 405

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "message": "unprocessable request",
      "error": 422
      }), 422

  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      "success": False,
      "message": "internal server error",
      "error": 500
    }), 500

  return app
