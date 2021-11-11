from flask import Flask, Blueprint
# from webserver.queries import Query as Q

# Client blueprint
cb = Blueprint('client', __name__, url_prefix='/client')


@cb.route('/')
def index():
    return "Client side working"


