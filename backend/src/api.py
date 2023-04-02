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
This endpoint serves to create a new drink, it is only accessible for roles with the post:drinks rights.
'''
@app.route("/drinks", methods=["POST"])
@requires_auth("post:drinks")
def postDrinks(payload):
    try: 
        # get details of new drink from request
        newDrink = request.get_json()
        drinkTitle = newDrink.get("title", None)
        drinkRecipe = newDrink.get("recipe", None)
        # check if recipe is only one ingredient and format it correctly
        if type(drinkRecipe) != list:
            drinkRecipe = [drinkRecipe]
        # create new drink item and push to database
        drinkToAdd = Drink(title=drinkTitle, recipe=json.dumps(drinkRecipe))
        drinkToAdd.insert()
        # return newly created item
        drink = drinkToAdd.long()
        return jsonify({
             "success": True,
             "drinks": drink
        })
    # errorhandling
    except Exception as e:
        if isinstance(e, HTTPException):
                abort(e.code)
        elif isinstance(e, AuthError):
                abort(e)
        else:
            abort(422)

'''
This endpoint serves to update the name, recipe or both of a given drink, it is only accessible for roles with the patch:drinks rights.
'''
@app.route("/drinks/<int:drinkId>", methods=["PATCH"])
@requires_auth("patch:drinks")
def patchDrink(payload, drinkId):
    try:
        # find drink in database and check if it exists
        drinkToUpdate = Drink.query.filter(Drink.id==drinkId).one_or_none()
        if drinkToUpdate is None:
            abort(404)
        # get values to update from request
        updateDrink = request.get_json()
        updateTitle = updateDrink.get("title", None)
        updateRecipe = updateDrink.get("recipe", None)
        # check if title must be updated and update it
        if updateTitle is not None:
            drinkToUpdate.title = updateTitle
        # check if recipe must be updated and update it
        if updateRecipe is not None:
            if type(updateRecipe) != list:
                updateRecipe = [updateRecipe]
            drinkToUpdate.recipe = json.dumps(updateRecipe)
        # update the database entry
        drinkToUpdate.update()
        drink = [drinkToUpdate.long()]
        # return updated drink
        return jsonify({
            "success": True,
            "drinks": drink
        })
    # errorhandling
    except Exception as e:
        if isinstance(e, HTTPException):
            abort(e.code)
        elif isinstance(e, AuthError):
            abort(e)
        else:
            abort(422)
    
    
    

'''
This endpiont serves to delete a drink from the database, it is only accessible with the delete:drinks rights.
'''
@app.route("/drinks/<int:drinkId>", methods=["DELETE"])
@requires_auth("delete:drinks")
def deleteDrink(payload, drinkId):
    try:
        # get drink from database and check if it exists
        drinkToDelete = Drink.query.filter(Drink.id==drinkId).one_or_none()
        if drinkToDelete is None:
            abort(404)
        # delete drink and return id of deleted drink
        drinkToDelete.delete()
        return jsonify({
            "success": True,
            "delete": drinkId
        })
    # errorhandling
    except Exception as e:
        if isinstance(e, HTTPException):
                abort(e.code)
        elif isinstance(e, AuthError):
                abort(e)
        else:
            abort(422)

# Error Handling
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

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

@app.errorhandler(AuthError)
def unauthorizedException(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error
    }), error.status_code