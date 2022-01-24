CREATE TYPE AddressType AS (
  street VARCHAR(20),
  city VARCHAR(20),
  state VARCHAR(10),
  zip_code VARCHAR(5)
);


CREATE TYPE ServiceType AS (
  service_id int,
  service_name VARCHAR(40),
  service_description text,
  location AddressType
);


CREATE TABLE Services_Offered OF ServiceType (
  PRIMARY KEY (service_id)
);


INSERT INTO Services_Offered VALUES (
        1,
        'Hungarian Pastry Shop',
        'Historic Cafe where number of books have been written by authors while sitting in the café',
        ROW('7984 Odio Rd.', 'Erie', 'Pennsylvania', '87858')::AddressType
);


CREATE TYPE AppointmentDurationType AS (
    time_entered TIMESTAMP,
    time_left TIMESTAMP,
    time_spent_in_minutes int
);


CREATE TYPE AppointmentType AS (
  appointment_id int,
  client_name             VARCHAR(40),
  service_provider_id    int,
  employee_name VARCHAR(40),
  appointment_status VARCHAR(10),
  appointment_duration AppointmentDurationType
);


CREATE TABLE Appointment_Summary OF AppointmentType (
  PRIMARY KEY (appointment_id),
  CONSTRAINT FK_service_provider
        FOREIGN KEY (service_provider_id) REFERENCES services_offered(service_id)
);


INSERT INTO Appointment_Summary VALUES (
      1,
      'Flavia Leblanc',
      1,
      'Scarlet Merrill',
      'Booked',
      ROW('2021-10-23 10:00:00', '2021-10-23 11:12:00')::AppointmentDuration
);
