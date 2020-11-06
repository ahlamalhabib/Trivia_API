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

 
  @app.route('/categories')
  def get_categories():
      #Create an endpoint to handle GET requests for all available categories.
      #Get all categories from the database.
      categories = Category.query.all()
      #if categories contains no item.
      if len(categories) == 0:
            abort(404)
      return jsonify({
            'success':True,
            #To print all categories.
            'categories': [ category.format() for category in categories]
      })
    

  @app.route('/questions')
  def get_questions():
    #Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). 
    #Get all Questions from the database.
    questions = Question.query.all()
    #to including pagination on questions.
    current_question = paginate_questions(request, questions)

    if len(current_question) == 0 :
      abort(404)

    return jsonify({
      'success': True, 
      'questions': current_question,
      'total_questions': len(questions)
      
    })


  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    #Create an endpoint to DELETE question using a question ID. 

    # Get question with spesific question id from the database.
    question = Question.query.get(question_id)
    
    try:
        question.delete()
        return jsonify({
          'success':True,
          'message': 'successfully deleted'
        })
    except:
      abort(422)


 
  @app.route('/questions', methods=['POST'])
  def create_question():
    #Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
    body = request.get_json()
    # to save all the attribute of the question.
    new_question = body.get('question')
    new_answer = body.get('answer')
    new_difficulty = body.get('difficulty')
    new_category = body.get('category')
    

    try:
        # insert the new question .
        question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
        question.insert()

        return jsonify({
          'success': True,
          'message': 'successfully created!',
          'total_questions': len(Question.query.all())
        })

    except :
       abort(422)


  
   
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
      #Create a POST endpoint to get questions based on a search term.
      body= request.get_json()
      search_term = body.get('searchTerm', '')

      #https://stackoverflow.com/questions/35030142/flask-restful-search-query
      questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
      #to including pagination on questions.
      current_question= paginate_questions(request, questions)
      # check if searched question not found.
      if (len(current_question) == 0):
         abort(404)

          

      return jsonify({
            'success': True,
            'questions': current_question,
            'total_questions': len(Question.query.all())
      })

     

 
  
  @app.route('/categories/<int:id>/questions')
  def get_questions_by_category(id):
    #Create a GET endpoint to get questions based on category.

    # Get category with spesific category id from the database.
    category = Category.query.get(id)
    
    
    try: 
        # get all question  that have the same category . 
        questions = Question.query.filter(Question.category == category.id).all()
        #to including pagination on questions.
        paginated_questions = paginate_questions(request, questions)

        return jsonify({
          'success': True,
          'questions': paginated_questions,
          'total_questions': len(questions),
          'current_category': category.id
         })
    except:
      abort(422)


 
  
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
      #Create a POST endpoint to get questions to play the quiz. 
      body = request.get_json()
      #take category and previous question parameters.
      previous_questions = body.get('previous_questions')
      quiz_category = body.get('quiz_category')

      try:
         #return questions within the given category, and that is not one of the previous questions.
         questions = Question.query.filter(Question.category == quiz_category['id'], Question.id.notin_(previous_questions)).first()
         return jsonify({
            'success': True,
            'question': questions.format()
         })
      except:
        abort(400)


  
  #Create error handlers for all expected errors 
  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
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
            'message': 'Unprocessable'
      }), 422


  return app

    