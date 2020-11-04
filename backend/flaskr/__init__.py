import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start= (page - 1)* QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE 
  questions = [question.format() for question in selection]
  current_question =  questions[start:end]
  return current_question

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources={'/': {'origins': '*'}})
  

  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers','Content-Type, Authorization, true')
      response.headers.add('Access-Control-Allow-Methods','GET, POST, PATCH, DELETE, OPTIONS')
      return response

 
  #Create an endpoint to handle GET requests for all available categories.
  @app.route('/categories')
  def get_categories():
      
      categories = Category.query.all()
      if len(categories) == 0:
            abort(404)
      formatted_categories = [ category.format() for category in categories]
      return jsonify({
            'success':True,
            'categories': formatted_categories
      }), 200
    

 #Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). 
  @app.route('/questions')
  def get_all_questions():
    questions = Question.query.order_by(Question.id).all()
    total_questions = len(questions)
    categories = Category.query.order_by(Category.id).all()

    current_question = paginate_questions(request, questions)
    if (len(current_question)) == 0 :
      abort(404)


    formatted_categories= {}
    for category in categories:
      formatted_categories[category.id] = category.type

    return jsonify({
      'success': True, 
      'question': current_question,
      'total_questions': total_questions,
      'category': formatted_categories,
      'current_category': None
    }), 200


  #Create an endpoint to DELETE question using a question ID. 
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
        question = Question.query.get(question_id)
        question.delete()
        return jsonify({
          'success':True,
          'deleted': question_id,
        }),200
    except:
      abort(422)


 
  #Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()
    if not ('question' in body and 'answer' in body and 'difficulty' in body and 'category' in body):
        abort(422)

    new_question = body.get('question')
    new_answer = body.get('answer')
    new_difficulty = body.get('difficulty')
    new_category = body.get('category')
    

    try:
        question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
        question.insert()

        return jsonify({
          'success': True,
          'message': 'Question successfully created!',
          'total_questions': len(Question.query.all())
        }), 201

    except :
       abort(422)


  
  #Create a POST endpoint to get questions based on a search term. 
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
      body= request.get_json()
      search_term = body.get('searchTerm', '')
      if search_term == '':
            abort(422)
      try:
          questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

          if len(questions) == 0:
                abort(404)

          paginated_questions = paginate_questions(request, questions)

          return jsonify({
                'success': True,
                'questions': paginated_questions,
                'total_questions': len(Question.query.all())
          }), 200

      except:
           abort(404)

 
  #Create a GET endpoint to get questions based on category. 
  @app.route('/categories/<int:id>/questions')
  def get_questions_by_category(id):
    category = Category.query.filter_by(id=id).one_or_none()
    if (category is None):
         abort(422)

    questions = Question.query.filter_by(category=id).all()

        # paginate questions
    paginated_questions = paginate_questions(
            request, questions)

    return jsonify({
        'success': True,
        'questions': paginated_questions,
        'total_questions': len(questions),
        'current_category': category.type
    })


 
  #Create a POST endpoint to get questions to play the quiz. 
  @app.route('/quizzes', methods=['POST'])
  def play_quiz_question():
      #copyright https://github.com/EmmanuelSage/trivia-api
      # process the request data and get the values
      data = request.get_json()
      previous_questions = data.get('previous_questions')
      quiz_category = data.get('quiz_category')

      if ((quiz_category is None) or (previous_questions is None)):
         abort(400)

        # if default value of category is given return all questions
        # else return questions filtered by category
      if (quiz_category['id'] == 0):
         questions = Question.query.all()
      else:
         questions = Question.query.filter_by(
         category=quiz_category['id']).all()

        # defines a random question generator method
      def get_random_question():
          return questions[random.randint(0, len(questions)-1)]

        # get random question for the next question
      next_question = get_random_question()

        # defines boolean used to check that the question
        # is not a previous question
      found = True

      while found:
          if next_question.id in previous_questions:
               next_question = get_random_question()
          else:
              found = False

      return jsonify({
          'success': True,
          'question': next_question.format()
      }), 200

  
  #Create error handlers for all expected errors 
  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request error'
      }), 400

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
      }), 404

    @app.errorhandler(422)
  def unprocesable_entity(error):
      return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable entity'
      }), 422


  return app

    