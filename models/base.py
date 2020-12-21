from core import db
from datetime import datetime as dt

def commit(obj):
    """
    Function for convenient commit
    """
    db.session.add(obj)
    db.session.commit()
    db.session.refresh(obj)

    return obj


class Model(object):
    @classmethod
    def create(cls, **kwargs):
        """
        Create new record

        cls: class
        kwargs: dict with object parameters
        """
        obj = cls(**kwargs)
        return commit(obj)

    @classmethod
    def update(cls, row_id, **kwargs):
        """
        Update record by id

        cls: class
        row_id: record id
        kwargs: dict with object parameters
        """
        obj = cls.query.filter_by(id=row_id).first()
        for key in kwargs:
            setattr(obj, key, kwargs[key])
        return commit(obj)


        # obj = cls.query.filter_by(id=row_id).first()
        # if obj:
        #     if 'name' in kwargs:
        #         obj.name = kwargs['name']
        #     if obj.__tablename__ == 'actors':
        #         if 'gender' in kwargs:
        #             obj.gender = kwargs['gender']
        #         if 'date_of_birth' in kwargs:
        #             obj.date_of_birth = kwargs['date_of_birth']
        #     elif obj.__tablename__ == 'movies':
        #         if 'year' in kwargs:
        #             obj.year = kwargs['year']
        #         if 'genre' in kwargs:
        #             obj.genre = kwargs['genre']
        #     return commit(obj)
        # else:
        #     return None
    
    @classmethod
    def delete(cls, row_id):
        """
        Delete record by id

        cls: class
        row_id: record id
        return: int (1 if deleted else 0)
        """
        # obj = cls.query.filter_by(id=row_id).first()
        # if obj:
        #     db.session.delete(obj)
        #     db.session.commit()
        #     return 1
        # else:
        #     return 0
        obj = cls.query.get(row_id)
        db.session.delete(obj)
        db.session.commit()
        return obj.name
    
    @classmethod
    def add_relation(cls, row_id, rel_obj):
        """
        Add relation to object

        cls: class
        row_id: record id
        rel_obj: related object
        """
        obj = cls.query.filter_by(id=row_id).first()
        if cls.__name__ == 'Actor':
            obj.filmography.append(rel_obj)
        elif cls.__name__ == 'Movie':
            obj.cast.append(rel_obj)
        return commit(obj)

    @classmethod
    def remove_relation(cls, row_id, rel_obj):
        """
        Remove certain relation

        cls: class
        row_id: record id
        rel_obj: related object
        """
        obj = cls.query.filter_by(id=row_id).first()
        if cls.__name__ == 'Actor':
            obj.filmography.remove(rel_obj)
        elif cls.__name__ == 'Movie':
            obj.cast.remove(rel_obj)
        return commit(obj)

    @classmethod
    def clear_relations(cls, row_id):
        """
        Remove all relations by id

        cls: class
        row_id: record id
        """
        # obj = cls.query.filter_by(id=row_id).first()
        # if cls.__name__ == 'Actor':
        #     temp = obj.filmography.copy()
        # elif cls.__name__ == 'Movie':
        #     temp = obj.cast.copy()
        # for el in temp:
        #     cls.remove_relation(row_id, el)
        # return commit(obj)

        obj = cls.query.filter_by(id=row_id).first()
        if cls.__name__ == 'Actor':
            for i in obj.filmography:
                obj.filmography.remove(i)
        elif cls.__name__ == 'Movie':
            for i in obj.cast:
                obj.cast.remove(i)
        return commit(obj)

