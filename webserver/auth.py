from flask import Flask, Blueprint

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/')
def index():
    return "Auth Working"