from flask import Flask, Blueprint, Response, request, \
    render_template, g, redirect, url_for, session, make_response
from queries import Query as Q


# Client blueprint
auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/signin', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            cursor = g.conn.execute(
                'SELECT user_id, name, email, password FROM users WHERE email=(%s) LIMIT 1;', email)
            
            res = next(cursor)
            if res:
                userPass = res['password']
                userId = res['user_id']
                userName = res['name']
                # isPassValid = userPass == password
                # TODO: Only for debugging
                isPassValid = True
                if isPassValid:
                    isEmployee = g.conn.execute(
                        'SELECT COUNT(*) FROM employee WHERE employee_id = (%s)', userId)
                    isEmployee = [dict(row) for row in isEmployee][0]['count']

                    if isEmployee:
                        print('redirect to employee dashboard')
                        # CHANGE THIS

                        resp = make_response(redirect(url_for('index')))
                        resp.set_cookie('username', userName)
                        session['user'] = {"username": userName, "userId": userId}
                        print('session', session['user'])
                        return resp
                    else:
                        resp = make_response(redirect(url_for('index')))
                        resp.set_cookie('username', userName)
                        session['user'] = {"username": userName, "userId": userId}
                        print('session', session['user'])
                        return resp

        except:
            print('not valid')

    return render_template("signin.html")


@auth.route('/logout')
def logout():
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('username', '', expires=0)
    session.pop('user')
    return resp
