from flask import Flask, request
from flask import current_app as app

from controllers.actor import *
from controllers.movie import *


@app.route('/api/actors', methods=['GET'])
def actors():
    """
    Get all actors in db
    """
    return get_all_actors()


@app.route('/api/actor', methods=['GET', 'PUT', 'POST', 'DELETE'])
def actor():
    """
    Get actor by id
    """
    if request.method == 'GET':
        return get_actor_by_id()
    elif request.method == 'PUT':
        return update_actor()
    elif request.method == 'POST':
        return add_actor()
    elif request.method == 'DELETE':
        return delete_actor()
    else:
        err = 'Wrong request key!'
        return make_response(jsonify(error=err), 400)


@app.route('/api/actor-relations', methods=['PUT', 'DELETE'])
def actor_relations():
    """
    Get actor-relations by id
    """
    if request.method == 'DELETE':
        return actor_clear_relations()
    elif request.method == 'PUT':
        return actor_add_relation()
    else:
        err = 'Wrong request key!'
        return make_response(jsonify(error=err), 400)


@app.route('/api/movies', methods=['GET'])
def movies():
    """
    Get all movies in db
    """
    return get_all_movies()


@app.route('/api/movie', methods=['GET', 'PUT', 'POST', 'DELETE'])
def movie():
    """
    Get movie by id
    """
    if request.method == 'GET':
        return get_movie_by_id()
    elif request.method == 'PUT':
        return update_movie()
    elif request.method == 'POST':
        return add_movie()
    elif request.method == 'DELETE':
        return delete_movie()
    else:
        err = 'Wrong request key!'
        return make_response(jsonify(error=err), 400)


@app.route('/api/movie-relations', methods=['PUT', 'DELETE'])
def movie_relations():
    """
    Get movie-relations by id
    """
    if request.method == 'DELETE':
        return movie_clear_relations()
    elif request.method == 'PUT':
        return movie_add_relation()
    else:
        err = 'Wrong request key!'
        return make_response(jsonify(error=err), 400)

