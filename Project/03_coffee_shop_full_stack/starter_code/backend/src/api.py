import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth
"""Python Flask API Auth0 integration example
"""


app = Flask(__name__)
setup_db(app)
CORS(app)
'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    formatted_drinks = []
    for drink in drinks:
        formatted_drinks.append( drink.short() )
    return jsonify({
        'success': True,
        'drinks': formatted_drinks
        })

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    drinks = Drink.query.all()
    formatted_drinks = []
    for drink in drinks:
        formatted_drinks.append(drink.long())
    return jsonify({
        'success': True,
        'drinks': formatted_drinks
        })

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(token):
    try:
        content = request.get_json()
        new_drink_title = content.get('title')
        new_drink_recipe = json.dumps(content.get('recipe'))

        new_drink = Drink(title = new_drink_title, recipe = new_drink_recipe)
        new_drink.insert()

        drink = [new_drink.long()]
        return jsonify({
        'success':True,
        'drinks': drink
        })
    except:
        abort(422)

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:patch_id>', methods=['PATCH'])
@requires_auth("patch:drinks")
def patch_drinks(token, patch_id):
 try:
    content = request.get_json()
    patched_drink_title = content.get('title')
    patched_drink_recipe = json.dumps(content.get('recipe'))
    selected_drink = Drink.query.filter(Drink.id == patch_id).one_or_none()
    if selected_drink is None:
        abort(404)
    else:
      if 'title' in content:
        selected_drink.title = patched_drink_title
      elif 'recipe' in content:
        selected_drink.recipe = patched_drink_recipe

      selected_drink.update()
      formatted_drink = [selected_drink.long()]
    return jsonify({
        'success': True,
        'drinks': formatted_drink})
 except:
     abort(422)
'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:delete_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(token, delete_id):
       select_drink = Drink.query.filter(Drink.id == delete_id).one_or_none()
       if select_drink is None:
          abort(404)
       else:
          select_drink.delete()
       return jsonify({
        'success': True,
        'delete': select_drink.id
        })

# Error Handling
'''
Example error handling for unprocessable entity
'''

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
        }),404

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def AuthError(error):
    response = jsonify(error.error)
    response.status_code = error.status_code
    return response

