from flask import jsonify, make_response

from ast import literal_eval

from models import Movie, Actor
from settings.constants import MOVIE_FIELDS
from .parse_request import get_request_data


def get_all_movies():
    """
    Get list of all records
    """
    all_movies = Movie.query.all()
    movies = []
    for movie in all_movies:
        mv = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        movies.append(mv)
    return make_response(jsonify(movies), 200)


def get_movie_by_id():
    """
    Get record by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

        obj = Movie.query.filter_by(id=row_id).first()
        try:
            movie = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        return make_response(jsonify(movie), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


def add_movie():
    """
    Add new movie
    """
    data = get_request_data()
    ''
    if 'name' in data.keys():
        name = data['name']
        if 'genre' in data.keys():
            genre = data['genre']
            if 'year' in data.keys():
                year = data['year']
                # use this for 200 response code
                data_movie = {'name': name, 'genre': genre, 'year': year}
                try:
                    new_record = Movie.create(**data_movie)
                    new_movie = {k: v for k, v in new_record.__dict__.items() if k in MOVIE_FIELDS}
                    return make_response(jsonify(new_movie), 200)
                except:
                    err = 'Cant create movie'
                    return make_response(jsonify(error=err), 400)
            else:
                err = 'No year specified'
                return make_response(jsonify(error=err), 400)
        else:
            err = 'No genre specified'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'No name specified'
        return make_response(jsonify(error=err), 400)

def update_movie():
    """
    Update movie record by id
    """
    data = get_request_data()
    ''
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        if 'name' in data.keys():
            name = data['name']
            if 'genre' in data.keys():
                genre = data['genre']
                if 'year' in data.keys():
                    year = data['year']
        # use this for 200 response code
                    data_movie_upd = {'name': name, 'genre': genre, 'year': year}
                    try:
                        upd_record = Movie.update(row_id, **data_movie_upd)#id, data
                        upd_movie = {k: v for k, v in upd_record.__dict__.items() if k in MOVIE_FIELDS}
                        return make_response(jsonify(upd_movie), 200)
                    except:
                        err = 'Cant update movie'
                        return make_response(jsonify(error=err), 400)
                else:
                    err = 'No year specified'
                    return make_response(jsonify(error=err), 400)
            else:
                err = 'No genre specified'
                return make_response(jsonify(error=err), 400)
        else:
            err = 'No name specified'
            return make_response(jsonify(error=err), 400)


def delete_movie():
    """
    Delete movie by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

        try:
            Movie.delete(row_id)#id
            msg = 'Record successfully deleted'
            return make_response(jsonify(message=msg), 200)
        except:
            err = 'Problem with delete'
            return make_response(jsonify(error=err), 400)
    # use this for 200 response code
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


def movie_add_relation():
    """
    Add actor to movie's cast
    """
    data = get_request_data()
    ''
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        if 'relation_id' in data.keys():
            try:
                relation_id = int(data['relation_id'])
            except:
                err = 'Relation id must be integer'
                return make_response(jsonify(error=err), 400)
            try:
                rel_obj = Actor.query.filter_by(id=relation_id).first()
            except:
                err = 'No such actor'
                return make_response(jsonify(error=err), 400)
            # use this for 200 response code
            try:
                movie = Movie.add_relation(row_id, rel_obj)   # add relation here #id , film
                rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
                rel_movie['cast'] = str(movie.cast)
                return make_response(jsonify(rel_movie), 200)
            except:
                err = 'Problem with add relation'
                return make_response(jsonify(error=err), 400)
        else:
            err = 'No relation id specified'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)

def movie_clear_relations():
    """
    Clear all relations by id
    """
    data = get_request_data()
    ''
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
    # use this for 200 response code
        try:
            movie = Movie.clear_relations(row_id)   # clear relations here #id
            rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
            rel_movie['cast'] = str(movie.cast)
            return make_response(jsonify(rel_movie), 200)
        except:
            err = 'Problem with movie_clear_relations'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)
