from flask import Flask, Blueprint, request, render_template, g, redirect, Response, url_for, session
from queries import Query as Q


# Admin blueprint (ab)
ab = Blueprint('admin', __name__, url_prefix='/admin')


@ab.route('/', methods=['GET', 'POST'])
def index():
    context = {}
    print(session)
    user = session.get('user')
    context['username'] = user['username'] if user else None
    appointments = Q.get_appointments(user['userId'])
    employee_appointment_requests = g.conn.execute(appointments).mappings().all()
    context['employee_appointment_requests'] = employee_appointment_requests
    print("employee_appointment_requests: {}".format(employee_appointment_requests))
    return render_template('admin.html', **context)


@ab.route('/accept_appointment', methods=['POST'])
def accept_appointment():
    values = request.form.get('accept').split(", ")
    sid = values[0]
    cid = values[1]
    eid = values[2]
    print(sid, cid, eid)
    accept_appointment = Q.accept_appointment(sid, cid, eid)
    result = g.conn.execute(accept_appointment)
    return render_template("accept_appointment.html")


@ab.route('/reject_appointment', methods=['POST'])
def reject_appointment():
    values = request.form.get('reject').split(", ")
    sid = values[0]
    cid = values[1]
    eid = values[2]
    reject_appointment = Q.reject_appointment(sid, cid, eid)
    result = g.conn.execute(reject_appointment)
    return render_template("reject_appointment.html")
