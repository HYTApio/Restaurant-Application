from cmath import inf
from db import db

def get_all_restaurants():
    sql_code = "SELECT id, name FROM restaurants WHERE visible=1 ORDER BY name"
    return db.session.execute(sql_code).fetchall()

def get_restaurant_info(restaurant_id):
    sql_code = "SELECT r.name, u.name, ri.info, ri.openinghours, ri.address, r.visible FROM restaurants r, users u, restaurantinfo ri WHERE r.id=:restaurant_id AND r.id=ri.restaurant_id AND r.creator_id=u.id"
    return db.session.execute(sql_code, {"restaurant_id":restaurant_id}).fetchone()

def get_restaurant_review(restaurant_id):
    sql_code = "SELECT u.name, r.stars, r.comment FROM reviews r, users u WHERE r.user_id=u.id AND r.restaurant_id=:restaurant_id order by r.id"
    return db.session.execute(sql_code, {"restaurant_id":restaurant_id}).fetchall()

def add_review(restaurant_id, user_id, stars, comment):
    sql_code = "INSERT INTO reviews (user_id, restaurant_id, stars, comment) VALUES (:user_id, :restaurant_id, :stars, :comment)"
    db.session.execute(sql_code, {"user_id":user_id, "restaurant_id":restaurant_id, "stars":stars, "comment":comment})
    db.session.commit()

def user_restaurants(user_id):
    sql_code = "SELECT id, name FROM restaurants WHERE creator_id=:user_id AND visible=1 ORDER BY name"
    return db.session.execute(sql_code, {"user_id":user_id}).fetchall()

def remove_restaurant(restaurant_id, user_id):
    sql_code = "UPDATE restaurants SET visible=0 WHERE id=:id AND creator_id=:user_id"
    db.session.execute(sql_code, {"id":restaurant_id, "user_id":user_id})
    db.session.commit()

def add_restaurant(name, info, openinghours, address, creator_id):
    sql_code = "INSERT INTO restaurants (creator_id, name, visible) VALUES (:creator_id, :name, 1) RETURNING id"
    restaurant_id = db.session.execute(sql_code, {"creator_id":creator_id, "name":name}).fetchone()[0]
    sql_code = "INSERT INTO restaurantinfo (restaurant_id, info, openinghours, address) VALUES (:restaurant_id, :info, :openinghours, :address)"
    db.session.execute(sql_code, {"restaurant_id":restaurant_id, "info":info, "openinghours":openinghours, "address":address})
    db.session.commit()
    return restaurant_id

def search_restaurant(query):
    sql_code = "SELECT id, name FROM restaurants WHERE name LIKE :query AND visible=1 ORDER BY name"
    return db.session.execute(sql_code, {"query":'%'+query+'%'}).fetchall()