import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
with app.app_context():
    db_drop_and_create_all()

# ROUTES

'''
@Done implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route("/drinks", methods=["GET"])
def getDrinks():
    try:
        drinks = Drink.query.all()
        drinkList = [d.short() for d in drinks]
        return jsonify({
            "success": True,
            "drinks": drinkList
        })
    except:
        abort(404)

'''
@Done implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks-detail", methods=["GET"])
@requires_auth("get:drinks-detail")
def getDrinkDetail(payload):
    try:
        drinks = Drink.query.all()
        drinkList = [d.long() for d in drinks]
        return jsonify({
            "success": True,
            "drinks": drinkList
        })
    except Exception as e:
        if isinstance(e, HTTPException):
                abort(e.code)
        elif isinstance(e, AuthError):
                abort(401)
        else:
            abort(404)

'''
@Done implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''

@app.route("/drinks", methods=["POST"])
@requires_auth("post:drinks")
def postDrinks(payload):
    try: 
        newDrink = request.get_json()
        drinkTitle = newDrink.get("title", None)
        drinkRecipe = newDrink.get("recipe", None)
        if type(drinkRecipe) != list:
             drinkRecipe = [drinkRecipe]
        drinkToAdd = Drink(title=drinkTitle, recipe=json.dumps(drinkRecipe))
        drinkToAdd.insert()
        drink = drinkToAdd.long()
        return jsonify({
             "success": True,
             "drinks": drink
        })
    except Exception as e:
        if isinstance(e, HTTPException):
                abort(e.code)
        elif isinstance(e, AuthError):
                abort(e)
        else:
            abort(422)

'''
@Done implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks/<int:drinkId>", methods=["PATCH"])
@requires_auth("patch:drinks")
def patchDrink(payload, drinkId):
    try:
        drinkToUpdate = Drink.query.filter(Drink.id==drinkId).one_or_none()
        if drinkToUpdate is None:
            abort(404)
        updateDrink = request.get_json()
        updateTitle = updateDrink.get("title", None)
        updateRecipe = updateDrink.get("recipe", None)
        if updateTitle is not None:
            drinkToUpdate.title = updateTitle
        if updateRecipe is not None:
            if type(updateRecipe) != list:
                updateRecipe = [updateRecipe]
            drinkToUpdate.recipe = json.dumps(updateRecipe)
        drinkToUpdate.update()
        drink = drinkToUpdate.long()
        return jsonify({
            "success": True,
            "drinks": drink
        })
    except Exception as e:
        if isinstance(e, HTTPException):
            abort(e.code)
        elif isinstance(e, AuthError):
            abort(e)
        else:
            abort(422)
    
    
    

'''
@Done implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks/<int:drinkId>", methods=["DELETE"])
@requires_auth("delete:drinks")
def deleteDrink(payload, drinkId):
    try:
        drinkToDelete = Drink.query.filter(Drink.id==drinkId).one_or_none()
        if drinkToDelete is None:
            abort(404)
        drinkToDelete.delete()
        return jsonify({
            "success": True,
            "delete": drinkId
        })
    except Exception as e:
        if isinstance(e, HTTPException):
                abort(e.code)
        elif isinstance(e, AuthError):
                abort(e)
        else:
            abort(422)

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
@Done implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@Done implement error handler for 404
    error handler should conform to general task above
'''

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "not found"
    }), 404

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Not authorized"
    }), 401
'''
@Done implement error handler for AuthError
    error handler should conform to general task above
'''

@app.errorhandler(AuthError)
def unauthorizedException(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error
    }), error.status_code