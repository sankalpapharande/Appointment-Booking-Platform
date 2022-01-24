/* Query 1:  Get the location of businesses who are open within a certain time range. */
SELECT L.street, L.city, L.state FROM Location L INNER JOIN Provider P ON P.location_id = L.location_id INNER JOIN Operating_Hours OH ON P.provider_id=OH.provider_id WHERE OH.open_at >= 1000 AND OH.close_at<=1400;

/* Query 2: Find all businesses whose employees have a rating above 5. */
SELECT P1.name FROM Provider P1 INNER JOIN Employee E2 ON P1.provider_id = E2.provider_id INNER JOIN Employee_Ratings R3 ON E2.employee_id=R3.employee_id WHERE R3.rating >5;

/* Query 3: Find cities and their corresponding businesses average pricing (across all services that its employees offer) where appointments have been made by clients. */
SELECT L.city, AVG(S.cost) AS avg_service_cost FROM Location L INNER JOIN Provider P ON P.location_id = L.location_id INNER JOIN Employee E ON P.provider_id=E.provider_id INNER JOIN Appointments A ON E.employee_id=A.employee_id INNER JOIN Service_Offerings S ON A.service_id=S.service_id GROUP BY L.city;