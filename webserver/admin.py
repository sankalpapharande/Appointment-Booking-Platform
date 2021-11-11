from flask import Flask, Blueprint


# Admin blueprint (ab)
ab = Blueprint('admin', __name__, url_prefix='/admin')


@ab.route('/')
def index():
    return "Admin Working"