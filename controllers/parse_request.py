from flask import request


def get_request_data():
    return request.form.to_dict()
