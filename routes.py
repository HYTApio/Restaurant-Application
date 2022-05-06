from flask import render_template, request, redirect
from users import login, register, require_role, logout, check_csrf, user_id
from restaurants import remove_restaurant, add_restaurant, get_restaurant_info, search_restaurant, update_restaurant, get_all_restaurants, user_restaurants
from app import app
from reviews import add_review, get_restaurant_review
from foods import add_alacartefood, add_lunchfood, get_alacartefood, get_lunchfood


@app.route("/")
def index():
    """Koti sivu

    Returns:
        Avaa index.html
    """
    return render_template("index.html", restaurants=get_all_restaurants())


@app.route("/restaurant/<int:restaurant_id>")
def show_restaurant_route(restaurant_id):
    """Ravintolan sivu

    Args:
    restaurant_id: Ravintolan tunnus

    Returns:
        Avaa restaurant.html
    """
    info = get_restaurant_info(restaurant_id)
    if not info:
        return redirect("/")

    if info[5] == 0:
        return redirect("/")

    reviews = get_restaurant_review(restaurant_id)
    alacarte = get_alacartefood(restaurant_id)
    lunch = get_lunchfood(restaurant_id)
    return render_template("restaurant.html", id=restaurant_id, name=info[0], creator=info[1], info=info[2], openinghours=info[3], address=info[4], reviews=reviews, creator_id=info[6], alacarte=alacarte, lunch=lunch)


@app.route("/logout")
def logout_route():
    """Kirjautuminen ulos

    Returns:
        Avaa index.html
    """
    logout()
    return redirect("/")


@app.route("/register", methods=["get", "post"])
def register_route():
    """Rekisteröitymissivu

    Returns:
        Avaa register.html
        Avaa index.html
        Avaa error.html
    """
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 5 or len(username) > 15:
            return render_template("error.html", message="Käyttäjänimessä tulee olla 5-15 merkkiä")

        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eivät täsmää")
        if len(password1) < 5:
            return render_template("error.html", message="Salasanan pitää olla vähintään 5 merkkiä pitkä")

        role = request.form["role"]
        if role not in ("1", "2"):
            return render_template("error.html", message="Väärä käyttäjärooli")

        if not register(username, password1, role):
            return render_template("error.html", message="Käyttäjä nimi on jo käytössä")

        return redirect("/")


@app.route("/login", methods=["get", "post"])
def login_route():
    """Kirjautumis sivu

    Returns:
        Avaa login.html
        Avaa index.html
        Avaa error.html
    """
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not login(username, password):
            return render_template("error.html", message="Väärä tunnus tai salasana")

        return redirect("/")


@app.route("/review", methods=["post"])
def review_route():
    """Arvostelusivu

    Returns:
        Avaa ravintolan sivun
    """
    check_csrf()
    restaurant_id = request.form["restaurant_id"]
    stars = int(request.form["stars"])
    if stars < 1 or stars > 5:
        return render_template("error.html", message="Tähtimäärä voi olla 1-5")

    comment = request.form["comment"]
    if len(comment) > 500:
        return render_template("error.html", message="Kommentti on liian pitkä")

    if comment == "":
        comment = "-"

    add_review(restaurant_id, user_id(), stars, comment)
    return redirect("/restaurant/"+str(restaurant_id))


@app.route("/remove", methods=["get", "post"])
def remove_restaurant_route():
    """Ravintolan poisto

    Returns:
        Avaa index.html
        Avaa remove.html
    """
    require_role(2)
    if request.method == "GET":
        restaurants = user_restaurants(user_id())
        return render_template("remove.html", restaurants=restaurants)

    if request.method == "POST":
        check_csrf()
        if "restaurant" in request.form:
            restaurant = request.form["restaurant"]
            remove_restaurant(restaurant, user_id())

        return redirect("/")


@app.route("/add", methods=["get", "post"])
def add_restaurant_route():
    """Ravintolan lisäys sivu

    Returns:
        Avaa ravintolan sivun
        Avaa add.html
        Avaa error.html
    """
    require_role(2)
    if request.method == "GET":
        return render_template("add.html")

    if request.method == "POST":
        check_csrf()
        name = request.form["name"]
        if len(name) > 25:
            return render_template("error.html", message="Ravintolan nimessä saa korkeintaan olla 25 merkkiä")

        if len(name) < 1:
            return render_template("error.html", message="Ravintolalla pitää olla nimi")

        searchname = name.lower()

        info = request.form["info"]
        if len(info) > 1000:
            return render_template("error.html", message="Infossa saa korkeintaan olla 1000 merkkiä")

        if info == "":
            info = "-"

        openinghours = request.form["openinghours"]
        if len(openinghours) > 100:
            return render_template("error.html", message="Aukioloajassa saa korkeintaan olla 1000 merkkiä")

        if openinghours == "":
            openinghours = "ei tietoa"

        address = request.form["address"]
        if len(address) > 100:
            return render_template("error.html", message="Osoite saa korkeintaan olla 100 merkkiä")

        if address == "":
            address = "ei tietoa"

        restaurant_id = add_restaurant(
            name, info, openinghours, address, user_id(), searchname)
        return redirect("/restaurant/"+str(restaurant_id))


@app.route("/search", methods=["get"])
def search_route():
    """Etsimis sivu

    Returns:
        Avaa search.html
    """
    query = request.args['query']
    query_help = query.lower()
    return render_template("search.html", restaurants=search_restaurant(query_help), search=query)


@app.route("/update_info", methods=["post"])
def update_info_route():
    """Päivitys sivu

    Returns:
        Avaa error.html
        Avaa ravintolan sivun
    """
    check_csrf()
    name = request.form["name"]
    if len(name) > 25:
        return render_template("error.html", message="Ravintolan nimessä saa korkeintaan olla 25 merkkiä")

    if len(name) < 1:
        return render_template("error.html", message="Ravintolalla pitää olla nimi")

    searchname = name.lower()

    info = request.form["info"]
    if len(info) > 1000:
        return render_template("error.html", message="Infossa saa korkeintaan olla 1000 merkkiä")

    if info == "":
        info = "-"

    openinghours = request.form["openinghours"]
    if len(openinghours) > 100:
        return render_template("error.html", message="Aukioloajassa saa korkeintaan olla 1000 merkkiä")

    if openinghours == "":
        openinghours = "ei tietoa"

    address = request.form["address"]
    if len(address) > 100:
        return render_template("error.html", message="Osoite saa korkeintaan olla 100 merkkiä")

    if address == "":
        address = "ei tietoa"

    restaurant_id = request.form["restaurant_id"]
    update_restaurant(
        name, info, openinghours, address, user_id(), restaurant_id, searchname)
    return redirect("/restaurant/"+str(restaurant_id))


@app.route("/add_alacartefood", methods=["post"])
def add_alacartefoo_route():
    """Alacarte ruuan lisäys

    Returns:
        Avaa error.html
        Avaa ravintolan sivun
    """
    check_csrf()
    name = request.form["name"]
    if len(name) > 25:
        return render_template("error.html", message="Ruuan nimessä saa korkeintaan olla 25 merkkiä")

    if len(name) < 1:
        return render_template("error.html", message="Ruualla pitää olla nimi")

    price = request.form["price"]
    if price:
        try:
            if float(price) < 0:
                return render_template("error.html", message="Hinnan pitää olla positiivinen numero")
        except:
            return render_template("error.html", message="Hinnan pitää olla positiivinen numero")
    else:
        return render_template("error.html", message="Ruualla pitää olla hinta")

    restaurant_id = request.form["restaurant_id"]
    add_alacartefood(name, price, restaurant_id)
    return redirect("/restaurant/"+str(restaurant_id))


@app.route("/add_lunchfood", methods=["post"])
def add_lunchfood_route():
    """Lounas ruuan lisäys

    Returns:
        Avaa error.html
        Avaa ravintolan sivun
    """
    check_csrf()
    name = request.form["name"]
    if len(name) > 25:
        return render_template("error.html", message="Ruuan nimessä saa korkeintaan olla 25 merkkiä")

    if len(name) < 1:
        return render_template("error.html", message="Ruualla pitää olla nimi")

    price = request.form["price"]
    if price:
        try:
            if float(price) < 0:
                return render_template("error.html", message="Hinnan pitää olla positiivinen numero")
        except:
            return render_template("error.html", message="Hinnan pitää olla positiivinen numero")
    else:
        return render_template("error.html", message="Ruualla pitää olla hinta")

    restaurant_id = request.form["restaurant_id"]
    add_lunchfood(name, price, restaurant_id)
    return redirect("/restaurant/"+str(restaurant_id))
