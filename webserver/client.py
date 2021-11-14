from flask import Flask, Blueprint, request, render_template, g, redirect, Response, url_for, session, json
from queries import Query as Q

import datetime as dt
from queries import Query as Q
from utils import generate_hours
import os

# Client blueprint
cb = Blueprint('client', __name__, url_prefix='/client')

static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
serviceMap = os.path.join(static_dir, "servicesMap.json")


@cb.route('/', methods=['GET', 'POST'])
def index():
    print(request.method)
    context = {}
    user = session.get('user')
    context['username'] = user['username'] if user else None
    providerQ = Q.get_all_providers()
    locationQ = Q.get_all_locations()
    
    provider_cursor = g.conn.execute(providerQ)
    location_cursor = g.conn.execute(locationQ)
    
    context['biz_types'] = [row[0] for row in provider_cursor]
    context['locations'] = [(city, state) for state, city in location_cursor]

    if request.method == 'POST':
        type = request.form.get('type')
        location = request.form.get('location')
        time = request.form.get('time')

        # Formate time
        startRange = endRange = ''
        if time:
            startRange = dt.datetime.strptime(time, "%Y-%m-%d")    
            endRange = startRange + dt.timedelta(days=1)
        
        # Format location
        type = type if type != 'Service Type' else ''
        city, state = '', ''
        if location != 'Location':
            location = location.split('||')
            city, state = location[0], location[1]

        businessesQ = Q.get_businesses(type, city, state, startRange, endRange)

        cursor = g.conn.execute(businessesQ)
        biz_list = []
        for row in cursor:
            type, name, street, city, state, \
                provider_id, open_at, close_at = row
            
            open_at_secs = dt.timedelta(minutes=open_at)
            open_at_hour = open_at_secs.seconds//3600
            open_at_minutes = (open_at_secs.seconds//60)%60
            
            close_at_secs = dt.timedelta(minutes=close_at)
            close_at_hour = close_at_secs.seconds//3600
            close_at_minutes = (close_at_secs.seconds//60)%60
            openAt = f"{open_at_hour:02}:{open_at_minutes:02}"
            closeAt = f"{close_at_hour:02}:{close_at_minutes:02}"
    
            biz = {
                "provider_id": provider_id,
                "type": type,
                "name": name,
                "address": street+', '+city+', '+state,
                "openAt": openAt,
                "closeAt": closeAt
            }
            biz_list.append(biz)

        context['biz_list'] = biz_list

    return render_template("index.html", **context)


@cb.route('/<provider_id>', methods=['GET', 'POST'])
def book(provider_id):
    context = {}
    user = session.get('user')
    context['username'] = user['username'] if user else None

    employeeQ = Q.get_employees(provider_id)
    providerQ = Q.get_provider(provider_id)
    employees = g.conn.execute(employeeQ).mappings().all()
    provider = g.conn.execute(providerQ).mappings().all()[0]
    
    all_services = json.load(open(serviceMap))
    context['employees'] = employees
    context['provider_name'] = provider['name']
    context['provider_services'] = all_services[provider['type']]

    if request.method == 'POST':
        selected_employee = request.form.get('employee_select')
        selected_service  = request.form.get('service_select')
        selected_datetime = request.form.get('date')
        selected_time     = request.form.get('time')

        if selected_service != 'Select service':
            serviceQ = Q.get_service(selected_service)
            serviceRecord = g.conn.execute(serviceQ).mappings().all()[0]
            context['service'] = serviceRecord
        
        if selected_time:
            # If a user is logged in
            if user:
                clientId = user['userId']
                datetime_str = selected_datetime + ' ' + selected_time

                apptDatetime = dt.datetime.strptime(datetime_str, "%A, %B %d %Y %H:%M")
                serviceId = serviceRecord['service_id']
                addApptQ = Q.add_appointment(apptDatetime, serviceId, selected_employee, clientId)
                
                try:
                    g.conn.execute(addApptQ)
                except:
                    print('Database error')

                session['appointments'] = {
                    'user': user,
                    "datetime": datetime_str,
                    "employee": selected_employee}
                return redirect(url_for('client.confirm'))
        else:
            if selected_employee != 'Select staff member':
                startRange = dt.datetime.now()
                if selected_datetime:
                    startRange = dt.datetime.strptime(selected_datetime, "%Y-%m-%d")
                
                endRange = startRange + dt.timedelta(days=1)
                
                query = Q.get_unavailable_dates(selected_employee, startRange, endRange)
                appt_cursor = g.conn.execute(query)
                
                unavailable_dates = set()
                for date in appt_cursor:
                    unavailable_dates.add((date[0].hour, date[0].minute))

                times = generate_hours(startRange, endRange, dt.timedelta(minutes=30))
                timeslots = []
                for time in times:
                    disabled = (time.hour, time.minute) in unavailable_dates
                    data = (time.strftime("%H:%M"), disabled)
                    timeslots.append(data)

                # print([t[-1] for t in timeslots])
                # TODO: Diasbla the select option for unavailable dates
                context['selected_date'] = startRange.strftime("%A, %B %-d %Y")
                context['timeslots'] = timeslots
                context['selected_employee'] = selected_employee
                context['selected_datetime'] = selected_datetime
            # print(timeslots)

        # return redirect(url_for('client.confirm', date=selected_datetime))

    return render_template("book.html", **context)

@cb.route('/confirm', methods=['GET', 'POST'])
def confirm():
    context = {}
    user = session.get('user')
    appt = session.get('appointments')
    context['username'] = user['username'] if user else None
    context['datetime'] = appt['datetime']

    return render_template("confirm.html", **context)


@cb.route('/appointments', methods=['GET', 'POST'])
def appointments():
    context = {}
    user = session.get('user')
    apptsQ = Q.get_user_appointments(user['userId'])
    user_appts = g.conn.execute(apptsQ).mappings().all()

    context['username'] = user['username'] if user else None
    context['appointments'] = user_appts

    if request.method == 'POST':
        description = request.form.get("description")
        employee_id = request.form.get("employee_id")
        rate_score = request.form.get("rating")
        client_id = user['userId']
        
        addRatingQ = Q.add_rating(description, rate_score, client_id, employee_id)
        
        try:
            g.conn.execute(addRatingQ)
        except BaseException as err:
            print('Could not add rating ', err)
            pass

    return render_template("appointments.html", **context)

