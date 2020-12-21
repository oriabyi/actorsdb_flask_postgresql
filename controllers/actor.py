from flask import jsonify, make_response

from datetime import datetime as dt
from ast import literal_eval

from models import Actor, Movie
from settings.constants import ACTOR_FIELDS  # to make response pretty
from .parse_request import get_request_data


def get_all_actors():
    """
    Get list of all records
    """
    all_actors = Actor.query.all()
    actors = []
    for actor in all_actors:
        act = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        actors.append(act)
    return make_response(jsonify(actors), 200)


def get_actor_by_id():
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

        obj = Actor.query.filter_by(id=row_id).first()
        try:
            actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        return make_response(jsonify(actor), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


def add_actor():
    data = get_request_data()
    ''
    if 'name' in data.keys():
        name = data['name']
        if 'gender' in data.keys():
            gender = data['gender']
            if 'date_of_birth' in data.keys():
                date_of_birth = data['date_of_birth']
                try:
                    date_of_birth_d = dt.strptime(date_of_birth, '%d.%m.%Y').date()
                except:
                    err = 'Dont correct data'
                    return make_response(jsonify(error=err), 400)
                # use this for 200 response code
                data_actor = {'name': name, 'gender': gender, 'date_of_birth': date_of_birth_d}
                try:
                    new_record = Actor.create(**data_actor)
                    new_actor = {k: v for k, v in new_record.__dict__.items() if k in ACTOR_FIELDS}
                    return make_response(jsonify(new_actor), 200)
                except:
                    err = 'Cant create actor'
                    return make_response(jsonify(error=err), 400)
            else:
                err = 'No date_of_birth specified'
                return make_response(jsonify(error=err), 400)
        else:
            err = 'No gender specified'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'No name specified'
        return make_response(jsonify(error=err), 400)


def update_actor():
    """
    Update actor record by id
    """
    data = get_request_data()
    ''
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)
    keys = list(data.keys())
    keys.remove('id')
    for i in range(len(keys)):
        if keys[i] == 'date_of_birth':
            try:
                data['date_of_birth'] = dt.strptime(data['date_of_birth'], '%d.%m.%Y').date()
            except:
                err = 'Wrong data format'
                return make_response(jsonify(error=err), 400)
            continue
        elif keys[i] == 'name':
            continue
        elif keys[i] == 'gender':
            continue
        else:
            err = 'Wrong keys'
            return make_response(jsonify(error=err), 400)
    try:
        upd_record = Actor.update(row_id, **data)
        upd_actor = {k: v for k, v in upd_record.__dict__.items() if k in ACTOR_FIELDS}
        return make_response(jsonify(upd_actor), 200)
    except:
        err = 'Record with such id does not exist'
        return make_response(jsonify(error=err), 400)

    ### END CODE HERE ###


def delete_actor():
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

        try:
            Actor.delete(row_id)  # id
            msg = 'Record successfully deleted'
            return make_response(jsonify(message=msg), 200)
        except:
            err = 'Problem with delete'
            return make_response(jsonify(error=err), 400)
    # use this for 200 response code
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


def actor_add_relation():
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
                rel_obj = Movie.query.filter_by(id=relation_id).first()
            except:
                err = 'No such movie'
                return make_response(jsonify(error=err), 400)
            # use this for 200 response code
            try:
                actor = Actor.add_relation(row_id, rel_obj)  # add relation here #id , film
                rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
                rel_actor['filmography'] = str(actor.filmography)
                return make_response(jsonify(rel_actor), 200)
            except:
                err = 'Problem with add relation'
                return make_response(jsonify(error=err), 400)
        else:
            err = 'No relation id specified'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


def actor_clear_relations():
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        try:
            actor = Actor.clear_relations(row_id)  # clear relations here #id
            rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
            rel_actor['filmography'] = str(actor.filmography)
            return make_response(jsonify(rel_actor), 200)
        except:
            err = 'Problem with movie_clear_relations'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)
