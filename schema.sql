CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    password TEXT,
    role INTEGER
);

CREATE TABLE restaurants (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES users,
    name TEXT,
    searchname TEXT,
    visible INTEGER
);

CREATE TABLE restaurantinfo (
    id SERIAL PRIMARY KEY,
    restaurant_id INTEGER REFERENCES restaurants,
    info TEXT,
    openinghours TEXT,
    address TEXT
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    restaurant_id INTEGER REFERENCES restaurants,
    stars INTEGER,
    comment TEXT
);

CREATE TABLE MENU (
    restaurant_id INTEGER REFERENCES restaurants,
    foodname TEXT,
    price NUMERIC
)
