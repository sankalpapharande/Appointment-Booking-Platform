from os import stat


class Query:
    """ Query strings; needs to be executed """
    
    @staticmethod
    def get_unavailable_dates(employee, startRange='', endRange=''):
        query = f"SELECT datetime\
                  FROM appointments\
                  WHERE employee_id='{employee}' "
        if startRange and endRange:
            query += f"AND datetime >= '{startRange}' AND datetime <'{endRange}'"
        
        return query


    @staticmethod
    def get_employees(provider_id):
        """ Get employees that work for this provider """
        return f"SELECT employee_id, p.name, u.name \
                    FROM employee e \
                    INNER JOIN provider p ON e.provider_id=p.provider_id \
                    INNER JOIN users u ON e.employee_id=u.user_id \
                    WHERE p.provider_id = {provider_id}"

    @staticmethod
    def get_all_providers():
        return "SELECT DISTINCT(type) FROM provider"

    @staticmethod
    def get_provider(provider_id):
        return f"SELECT provider_id, name, type, location_id \
            FROM provider WHERE provider_id={provider_id} LIMIT 1;"

    @staticmethod
    def get_all_locations():
        return "SELECT state, city FROM location"

    
    @staticmethod
    def get_service(service_name):
        return f"SELECT service_id, name, duration, cost \
            FROM service_offerings\
            WHERE name='{service_name}'"

    @staticmethod
    def get_user_appointments(user_id):
        return f"SELECT datetime, status, so.name AS service_name,\
                        duration, cost, u.name AS employee_name, \
                        p.name as provider_name \
                FROM appointments a, service_offerings so, users u, \
                    employee e, provider p \
                WHERE a.employee_id = u.user_id AND \
                    a.employee_id = e.employee_id AND \
                    e.provider_id = p.provider_id AND \
                    a.service_id = so.service_id AND \
                    a.client_id = {user_id};"


    @staticmethod
    def get_businesses(biz_type, city, state, startRange='', endRange=''):
        baseQ = "SELECT p.type, p.name, l.street, l.city, l.state, p.provider_id, oh.open_at, oh.close_at \
                 FROM provider p, location l, employee e, appointments a, operating_hours oh \
                 WHERE p.location_id = l.location_id AND \
                       p.provider_id = e.provider_id AND \
                       e.employee_id = a.employee_id AND \
                       p.provider_id = oh.provider_id"
        

        typeQ  = f" AND p.type='{biz_type}'" if biz_type else ''
        stateQ = f" AND l.state='{state}'" if state else ''
        cityQ  = f" AND l.city='{city}'" if city else ''
        timeQ  = f" AND a.datetime NOT BETWEEN '{startRange}' AND '{endRange}'" \
            if startRange and endRange else ''
        fullQ  = baseQ + typeQ + stateQ + cityQ + timeQ
        return fullQ

    @staticmethod
    def add_appointment(datetime, serviceId, employeeId, clientId):
        return f" INSERT INTO appointments(datetime, status, service_id, employee_id, client_id)\
                VALUES ('{datetime}', 'Pending', {serviceId}, {employeeId}, {clientId})"



