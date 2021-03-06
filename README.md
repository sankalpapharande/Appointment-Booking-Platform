# coms4111-p1
Repository for Introduction to Databases (COMS4111) Project 1

35.243.128.11

The PostgreSQL account:  spa2138


The URL of your web application: http://35.243.128.11:8111/client/


 ## Project Overview ##
We developed a centralized on-demand appointment booking platform that will connect business providers with
users who are looking to schedule appointments.

The primary focus of this project is to execute a substantial real-world database application.

Flask Server can be initiated using :
```python3 server.py```

 ## Parts Implemented ##
1. Service Provider Dashboard
   1. View appointments
   2. Accept or reject the appointment request
2. Customers Dashboard
   1. View a list of all businesses
   2. Search and filter business based on service offered, availability, or location
   3. Make an appointment
   4. Leave a review/rating after the appointment

 ## Web Pages ##
1. admin/ : Service Provider Dashboard where employee can view the appointments
2. client/: Where customers can book the appointment

 ## Directory structure: ##
1. ``static``
   1. `js/script.js`: javascript code scripts.
   2. ``serviceMap.json``: mapping of services to business types
2. ``templates``: html templates for frontend
3. Entities:
   1. ``admin.py``: methods for admin role login functionalities
   2. ``client.py``: methods for client role login functionalities
   3. ``auth.py``: authentication functionalities
4. ``queries.py``: query class containing methods for all SQL queries
5. ``server.py``: flask python server
6. ``utils.py``: helper functions

 ## Entity-Relationship Diagram ##
![image](https://drive.google.com/uc?export=view&id=1BbcxQ31nMdtkoTsrTnFS-Wp3WHa3JxMu)
