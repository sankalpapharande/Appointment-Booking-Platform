from flask import Flask, Blueprint, request, render_template, g, redirect, Response, url_for, session
from queries import Query as Q


# Admin blueprint (ab)
ab = Blueprint('admin', __name__, url_prefix='/admin')


@ab.route('/')
def index():
    return "Admin Working"
