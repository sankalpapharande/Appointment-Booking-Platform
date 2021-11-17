
"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally: 
    python3 server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
from datetime import timedelta
import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, url_for, session

from client import cb
from admin import ab
from auth import auth

# Init Flask app
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
app.secret_key = 'supersecret'

# Register Blueprints
app.register_blueprint(cb)
app.register_blueprint(ab)
app.register_blueprint(auth)

# Create connection
DATABASEURI = "postgresql://spa2138:6082@34.74.246.148/proj1part2"
engine = create_engine(DATABASEURI)


@app.before_request
def before_request():
    """ Setup a db conn to be used for requests; g is globally accessible"""
    try:
        g.conn = engine.connect()
    except:
        print("uh oh, problem connecting to database")
        import traceback
        traceback.print_exc()
        g.conn = None


@app.teardown_request
def teardown_request(exception):
    """
    At the end of the web request, this makes sure to close the database connection.
    If you don't, the database could run out of memory!
    """
    try:
        g.conn.close()
    except Exception as e:
        pass

@app.route('/')
def index(): 
    return redirect('/client')

if __name__ == "__main__":
    import click

    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=8111, type=int)
    def run(debug, threaded, host, port):
        HOST, PORT = host, port
        print("running on %s:%d" % (HOST, PORT))
        app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

    run()
