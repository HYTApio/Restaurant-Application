from db import db


def add_alacartefood(name, price, restaurant_id):
    """Lisää alacarte menulle ruuan

    Args:
        name: Ruuan nimi
        price: Ruuan hinta
        restaurant_id: Ravintolan nimi mille lisätään
    """
    sql_code = "INSERT INTO alacartefood (foodname, price, restaurant_id) VALUES (:name, :price, :restaurant_id)"
    db.session.execute(
        sql_code, {"name": name, "price": price, "restaurant_id": restaurant_id})
    db.session.commit()


def get_alacartefood(restaurant_id):
    """Etsii kaikki alacarte ruuat

    Args:
        restaurant_id: Ravintolan nimi miltä haetaan

    Returns:
        Lista ruuista
    """
    sql_code = "SELECT foodname, price FROM alacartefood WHERE restaurant_id=:restaurant_id order by foodname"
    return db.session.execute(sql_code, {"restaurant_id": restaurant_id}).fetchall()


def add_lunchfood(name, price, restaurant_id):
    """Lisää lounas menulle ruuan

    Args:
        name: Ruuan nimi
        price: Ruuan hinta
        restaurant_id: Ravintolan nimi mille lisätään
    """
    sql_code = "INSERT INTO lunchfood (foodname, price, restaurant_id) VALUES (:name, :price, :restaurant_id)"
    db.session.execute(
        sql_code, {"name": name, "price": price, "restaurant_id": restaurant_id})
    db.session.commit()


def get_lunchfood(restaurant_id):
    """Etsii kaikki lounas ruuat

    Args:
        restaurant_id: Ravintolan nimi miltä haetaan

    Returns:
        Lista ruuista
    """
    sql_code = "SELECT foodname, price FROM lunchfood WHERE restaurant_id=:restaurant_id order by foodname"
    return db.session.execute(sql_code, {"restaurant_id": restaurant_id}).fetchall()
