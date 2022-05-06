from db import db


def get_all_restaurants():
    """Etsii kaikki ravintolat

    Returns:
        Lista ravintoloista
    """
    sql_code = "SELECT id, name FROM restaurants WHERE visible=1 ORDER BY name"
    return db.session.execute(sql_code).fetchall()


def get_restaurant_info(restaurant_id):
    """Etsii tietyn ravintolan tiedot

    Args:
        restaurant_id: Etsittävän ravintolan tunnus

    Returns:
        Tiedot ravintolasta
    """
    sql_code = "SELECT r.name, u.name, r.info, r.openinghours, r.address, r.visible, r.creator_id FROM restaurants r, users u WHERE r.id=:restaurant_id AND r.creator_id=u.id"
    return db.session.execute(sql_code, {"restaurant_id": restaurant_id}).fetchone()


def user_restaurants(user_id):
    """Etsii käyttäjän omistamat ravintolat

    Args:
        user_id: Käyttäjän tunnus

    Returns:
        Ravintoloiden id:t ja nimet
    """
    sql_code = "SELECT id, name FROM restaurants WHERE creator_id=:user_id AND visible=1 ORDER BY name"
    return db.session.execute(sql_code, {"user_id": user_id}).fetchall()


def remove_restaurant(restaurant_id, user_id):
    """Poistaa ravintolan

    Args:
        restaurant_id: Poistettavan ravintolan tunnus
        user_id: Poistavan käyttäjän tunnus
    """
    sql_code = "UPDATE restaurants SET visible=0 WHERE id=:id AND creator_id=:user_id"
    db.session.execute(sql_code, {"id": restaurant_id, "user_id": user_id})
    db.session.commit()


def add_restaurant(name, info, openinghours, address, creator_id, searchname):
    """Lisää ravintolan

    Args:
        name: Ravintolan nimi
        info: Ravintolan info
        openinghours: Ravintolan aukioloajat
        address: Ravintolan osoite
        creator_id: Ravintolan perustajan tunnus
        searchname: Ravintolaa etsiessä nimi on kaikki pienellä

    Returns:
        Ravintolan tunnus
    """
    sql_code = "INSERT INTO restaurants (creator_id, name, visible, searchname, info, openinghours, address) VALUES (:creator_id, :name, 1, :searchname, :info, :openinghours, :address) RETURNING id"
    restaurant_id = db.session.execute(sql_code, {
        "creator_id": creator_id, "name": name, "searchname": searchname, "info": info, "openinghours": openinghours, "address": address}).fetchone()[0]
    db.session.commit()
    return restaurant_id


def search_restaurant(query):
    """Etsii tietyn nimiset ravintolat

    Args:
        query: Hakusana

    Returns:
        Ravintolat joiden nimissä on hakusana
    """
    sql_code = "SELECT id, name FROM restaurants WHERE searchname LIKE :query AND visible=1 ORDER BY name"
    return db.session.execute(sql_code, {"query": '%'+query+'%'}).fetchall()


def update_restaurant(name, info, openinghours, address, creator_id, restaurant_id, searchname):
    """Päivittää ravintolan tiedot

    Args:
        name: Ravintolan nimi
        info: Ravintolan info
        openinghours: Ravintolan aukioloajat
        address: Ravintolan osoite
        creator_id: Ravintolan perustajan tunnus
        searchname: Ravintolaa etsiessä nimi on kaikki pienellä
    """
    sql_code = "UPDATE restaurants SET name=:name, searchname=:searchname, info=:info, openinghours=:openinghours, address=:address WHERE id=:restaurant_id"
    db.session.execute(sql_code, {"creator_id": creator_id, "name": name, "restaurant_id": restaurant_id,
                                  "searchname": searchname, "info": info, "openinghours": openinghours, "address": address})
    db.session.commit()

