from db import db

def get_all_restaurants():
    sql_code = "SELECT id, name FROM restaurants WHERE visible=1 ORDER BY name"
    return db.session.execute(sql_code).fetchall()

def get_restaurant_info(restaurant_id):
    sql_code = "SELECT r.name, u.name, r.info, r.openinghours, r.address, r.visible, r.creator_id FROM restaurants r, users u WHERE r.id=:restaurant_id AND r.creator_id=u.id"
    return db.session.execute(sql_code, {"restaurant_id":restaurant_id}).fetchone()

def get_restaurant_review(restaurant_id):
    sql_code = "SELECT u.name, r.stars, r.comment FROM reviews r, users u WHERE r.user_id=u.id AND r.restaurant_id=:restaurant_id order by r.id"
    return db.session.execute(sql_code, {"restaurant_id":restaurant_id}).fetchall()

def add_review(restaurant_id, user_id, stars, comment):
    sql_code = "SELECT * FROM reviews WHERE restaurant_id=:restaurant_id AND user_id=:user_id"
    if len(db.session.execute(sql_code, {"restaurant_id":restaurant_id, "user_id":user_id}).fetchall()) < 1:
        sql_code = "INSERT INTO reviews (user_id, restaurant_id, stars, comment) VALUES (:user_id, :restaurant_id, :stars, :comment)"
        db.session.execute(sql_code, {"user_id":user_id, "restaurant_id":restaurant_id, "stars":stars, "comment":comment})
        db.session.commit()
    
    else:
        sql_code = "UPDATE reviews SET stars=:stars, comment=:comment WHERE user_id=:user_id AND restaurant_id=:restaurant_id"
        db.session.execute(sql_code, {"user_id":user_id, "restaurant_id":restaurant_id, "stars":stars, "comment":comment})
        db.session.commit()

def user_restaurants(user_id):
    sql_code = "SELECT id, name FROM restaurants WHERE creator_id=:user_id AND visible=1 ORDER BY name"
    return db.session.execute(sql_code, {"user_id":user_id}).fetchall()

def remove_restaurant(restaurant_id, user_id):
    sql_code = "UPDATE restaurants SET visible=0 WHERE id=:id AND creator_id=:user_id"
    db.session.execute(sql_code, {"id":restaurant_id, "user_id":user_id})
    db.session.commit()

def add_restaurant(name, info, openinghours, address, creator_id, searchname):
    sql_code = "INSERT INTO restaurants (creator_id, name, visible, searchname, info, openinghours, address) VALUES (:creator_id, :name, 1, :searchname, :info, :openinghours, :address) RETURNING id"
    restaurant_id = db.session.execute(sql_code, {
    "creator_id":creator_id, "name":name, "searchname":searchname, "info":info, "openinghours":openinghours, "address":address}).fetchone()[0]
    db.session.commit()
    return restaurant_id

def search_restaurant(query):
    sql_code = "SELECT id, name FROM restaurants WHERE searchname LIKE :query AND visible=1 ORDER BY name"
    return db.session.execute(sql_code, {"query":'%'+query+'%'}).fetchall()

def has_review(restaurant_id, user_id):
    sql_code = "SELECT * FROM reviews WHERE restaurant_id=:restaurant_id AND user_id=:user_id"
    if len(db.session.execute(sql_code, {"restaurant_id":restaurant_id, "user_id":user_id})) > 1:
        return True
     
def update_restaurant(name, info, openinghours, address, creator_id, restaurant_id, searchname):
    sql_code = "UPDATE restaurants SET name=:name, searchname=:searchname, info=:info, openinghours=:openinghours, address=:address WHERE id=:restaurant_id"
    db.session.execute(sql_code, {"creator_id":creator_id, "name":name, "restaurant_id":restaurant_id, "searchname":searchname, "info":info, "openinghours":openinghours, "address":address})
    db.session.commit()

def add_alacartefood(name, price, restaurant_id):
    sql_code = "INSERT INTO alacartefood (foodname, price, restaurant_id) VALUES (:name, :price, :restaurant_id)"
    db.session.execute(sql_code, {"name":name, "price":price, "restaurant_id":restaurant_id})
    db.session.commit()

def get_alacartefood(restaurant_id):
    sql_code = "SELECT foodname, price FROM alacartefood WHERE restaurant_id=:restaurant_id order by foodname"
    return db.session.execute(sql_code, {"restaurant_id":restaurant_id}).fetchall()

def add_lunchfood(name, price, restaurant_id):
    sql_code = "INSERT INTO lunchfood (foodname, price, restaurant_id) VALUES (:name, :price, :restaurant_id)"
    db.session.execute(sql_code, {"name":name, "price":price, "restaurant_id":restaurant_id})
    db.session.commit()

def get_lunchfood(restaurant_id):
    sql_code = "SELECT foodname, price FROM lunchfood WHERE restaurant_id=:restaurant_id order by foodname"
    return db.session.execute(sql_code, {"restaurant_id":restaurant_id}).fetchall()  