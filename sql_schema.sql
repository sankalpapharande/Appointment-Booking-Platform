-- US based locations only, zip code should be 5 digits
CREATE TABLE Location
(
    location_id SERIAL,
    zip_code    VARCHAR(5) CHECK ( zip_code ~ '[0-9][0-9][0-9][0-9][0-9]'),
    street      VARCHAR(40),
    city        VARCHAR(20),
    state       VARCHAR(20),
    PRIMARY KEY (location_id)
);

CREATE TABLE Provider
(
    provider_id SERIAL,
    name        VARCHAR(40),
    type        VARCHAR(40),
    location_id INTEGER NOT NULL,
    PRIMARY KEY (provider_id),
    FOREIGN KEY (location_id)
        REFERENCES Location (location_id)
        ON DELETE NO ACTION
);

CREATE TABLE Users
(
    user_id  SERIAL,
    name     VARCHAR(40),
    email    VARCHAR(100) CHECK ( email ~ '%_@__%.__%' ),
    password VARCHAR(40),
    PRIMARY KEY (user_id)
);

-- SSN is a 9 digit number with format: 123-45-6789
-- Phone numbers: should not contain not digits, but can contain +,-
CREATE TABLE Employee
(
    ssn          CHAR(11) CHECK ( ssn ~ '[0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9]' ),
    phone_number CHAR(12) CHECK ( phone_number NOT LIKE '%[^0-9+-.]%'),
    employee_id  INTEGER,
    provider_id  INTEGER NOT NULL,
    PRIMARY KEY (employee_id),
    FOREIGN KEY (provider_id) REFERENCES Provider (provider_id),
    FOREIGN KEY (employee_id)
        REFERENCES Users (user_id)
        ON DELETE CASCADE
);

-- CREATE TABLE Client
-- (
--     client_id     SERIAL,
--     points_earned INTEGER,
--     PRIMARY KEY (client_id),
--     FOREIGN KEY (client_id)
--         REFERENCES Users (user_id)
--         ON DELETE CASCADE
-- );

CREATE TABLE Client
(
    client_id     INTEGER,
    points_earned INTEGER,
    PRIMARY KEY (client_id),
    FOREIGN KEY (client_id)
        REFERENCES Users (user_id)
        ON DELETE CASCADE
);

-- create table Service_Offerings
-- (
--     service_id  SERIAL,
--     name        VARCHAR(40),
--     duration    INTEGER,
--     cost        REAL CHECK ( cost > 0 ),
--     provider_id INTEGER,
--     PRIMARY KEY (service_id)
-- );


create table Service_Offerings
(
    service_id  SERIAL,
    name        VARCHAR(40),
    duration    INTEGER,
    cost        REAL CHECK ( cost > 0 ),
    PRIMARY KEY (service_id)
);


-- CREATE TABLE Appointments
-- (
--     datetime    DATE,
--     status      VARCHAR(10),
--     service_id  INTEGER,
--     employee_id INTEGER,
--     client_id   INTEGER,
--     PRIMARY KEY (service_id, employee_id, client_id),
--     FOREIGN KEY (service_id) REFERENCES Service_Offerings (service_id),
--     FOREIGN KEY (employee_id) REFERENCES Employee (employee_id),
--     FOREIGN KEY (client_id) REFERENCES Client (client_id)
-- );

CREATE TABLE Appointments
(
    datetime    TIMESTAMP,
    status      VARCHAR(10),
    service_id  INTEGER,
    employee_id INTEGER,
    client_id   INTEGER,
    PRIMARY KEY (service_id, employee_id, client_id),
    FOREIGN KEY (service_id) REFERENCES Service_Offerings (service_id),
    FOREIGN KEY (employee_id) REFERENCES Employee (employee_id),
    FOREIGN KEY (client_id) REFERENCES Client (client_id)
);


CREATE TABLE Employee_Ratings
(
    rating      INTEGER CHECK ( rating >= 0 AND rating <= 10 ),
    description VARCHAR(255),
    client_id   INTEGER,
    employee_id INTEGER,
    PRIMARY KEY (client_id, employee_id),
    FOREIGN KEY (client_id) REFERENCES Client (client_id),
    FOREIGN KEY (employee_id) REFERENCES Employee (employee_id)
);

-- open_at, close_at - integer of the number of minutes past midnight
-- both should be in the range [0, 1440) (1440 minutes in a day)
-- close_at should be greater than open_at
CREATE TABLE Operating_Hours
(
    day_of_week INTEGER,
    open_at     INTEGER CHECK ( open_at >= 0 AND open_at < 1440 ),
    close_at    INTEGER CHECK ( close_at > open_at AND close_at < 1440 ),
    provider_id INTEGER,
    PRIMARY KEY (provider_id, day_of_week),
    FOREIGN KEY (provider_id)
        REFERENCES Provider (provider_id)
        ON DELETE CASCADE
)