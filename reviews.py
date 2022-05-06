from db import db


def add_review(restaurant_id, user_id, stars, comment):
    """Lisää arvostelun ravintolalle

    Args:
        restaurant_id: Etsittävän ravintolan tunnus
        user_id: Arvioijan tunnus
        stars: Arvio tähdissä
        comment: Arvioijan kommentti
    """
    sql_code = "SELECT * FROM reviews WHERE restaurant_id=:restaurant_id AND user_id=:user_id"
    if len(db.session.execute(sql_code, {"restaurant_id": restaurant_id, "user_id": user_id}).fetchall()) < 1:
        sql_code = "INSERT INTO reviews (user_id, restaurant_id, stars, comment) VALUES (:user_id, :restaurant_id, :stars, :comment)"
        db.session.execute(sql_code, {
            "user_id": user_id, "restaurant_id": restaurant_id, "stars": stars, "comment": comment})
        db.session.commit()

    else:
        sql_code = "UPDATE reviews SET stars=:stars, comment=:comment WHERE user_id=:user_id AND restaurant_id=:restaurant_id"
        db.session.execute(sql_code, {
            "user_id": user_id, "restaurant_id": restaurant_id, "stars": stars, "comment": comment})
        db.session.commit()

def get_restaurant_review(restaurant_id):
    """Etsii tietyn ravintolan arvostelut

    Args:
        restaurant_id: Etsittävän ravintolan tunnus

    Returns:
        Arvostelut ravintolasta
    """
    sql_code = "SELECT u.name, r.stars, r.comment FROM reviews r, users u WHERE r.user_id=u.id AND r.restaurant_id=:restaurant_id order by r.id"
    return db.session.execute(sql_code, {"restaurant_id": restaurant_id}).fetchall()
