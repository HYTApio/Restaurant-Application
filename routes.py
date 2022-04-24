from app import app
from flask import render_template, request, redirect
import users, restaurants

@app.route("/")
def index():
    return render_template("index.html", restaurants=restaurants.get_all_restaurants())

@app.route("/restaurant/<int:restaurant_id>")
def show_restaurant(restaurant_id):
    info = restaurants.get_restaurant_info(restaurant_id)
    if not info:
        return redirect("/")

    if info[5]==0:
        return redirect("/")

    reviews = restaurants.get_restaurant_review(restaurant_id)
    menu = restaurants.get_restaurant_menu(restaurant_id)
    return render_template("restaurant.html", id=restaurant_id, name=info[0], creator=info[1], info=info[2], openinghours=info[3], address=info[4], reviews=reviews, creator_id=info[6], menu=menu)

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["get", "post"])
def register():
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
        if len(password1)<5:
            return render_template("error.html", message="Salasanan pitää olla vähintään 5 merkkiä pitkä")
        
        role=request.form["role"]
        if role not in ("1", "2"):
            return render_template("error.html", message="Väärä käyttäjärooli")

        if not users.register(username, password1, role):
            return render_template("error.html", message="Käyttäjä nimi on jo käytössä")
        
        return redirect("/")

@app.route("/login", methods=["get", "post"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not users.login(username, password):
            return render_template("error.html", message="Väärä tunnus tai salasana")
        
        return redirect("/")

@app.route("/review", methods=["post"])
def review():
    users.check_csrf()
    restaurant_id = request.form["restaurant_id"]
    stars = int(request.form["stars"])
    if 1 > stars or 5 < stars:
        return render_template("error.html", message="Tähtimäärä voi olla 1-5")
    
    comment = request.form["comment"]
    if len(comment) > 500:
        return render_template("error.html", message="Kommentti on liian pitkä")
    
    if comment=="":
        comment = "-"

    restaurants.add_review(restaurant_id, users.user_id(), stars, comment)
    return redirect("/restaurant/"+str(restaurant_id))

@app.route("/remove", methods=["get", "post"])
def remove_restaurant():
    users.require_role(2)
    if request.method == "GET":
        user_restaurants = restaurants.user_restaurants(users.user_id())
        return render_template("remove.html", restaurants=user_restaurants)
    
    if request.method == "POST":
        users.check_csrf()
        if "restaurant" in request.form:
            restaurant = request.form["restaurant"]
            restaurants.remove_restaurant(restaurant, users.user_id())
        
        return redirect("/")
    
@app.route("/add", methods=["get", "post"])
def add_restaurant():
    users.require_role(2)
    if request.method == "GET":
        return render_template("add.html")
    
    if request.method == "POST":
        users.check_csrf()
        name = request.form["name"]
        if len(name) > 25:
            return render_template("error.html", message="Ravintolan nimessä saa korkeintaan olla 25 merkkiä")
        
        if len(name) < 1:
            return render_template("error.html", message="Ravintolalla pitää olla nimi")
        
        searchname=name.lower()

        info = request.form["info"]
        if len(info) > 1000:
            return render_template("error.html", message="Infossa saa korkeintaan olla 1000 merkkiä")

        if info=="":
            info="-"

        openinghours = request.form["openinghours"]
        if len(openinghours) > 100:
            return render_template("error.html", message="Aukioloajassa saa korkeintaan olla 1000 merkkiä")

        if openinghours=="":
            openinghours="ei tietoa"
    
        address = request.form["address"]
        if len(address) > 100:
            return render_template("error.html", message="Osoite saa korkeintaan olla 100 merkkiä")
        
        if address=="":
            "ei tietoa"
        
        restaurant_id = restaurants.add_restaurant(name, info, openinghours, address, users.user_id(), searchname)
        return redirect("/restaurant/"+str(restaurant_id))
    
@app.route("/search", methods=["get"])
def search():
    query = request.args['query']
    query_help = query.lower()
    return render_template("search.html", restaurants=restaurants.search_restaurant(query_help), search=query)

@app.route("/update_info", methods=["post"])
def update_info():
    users.check_csrf()
    name = request.form["name"]
    if len(name) > 25:
        render_template("error.html", message="Ravintolan nimessä saa korkeintaan olla 25 merkkiä")
     
    if len(name) < 1:
        render_template("error.html", message="Ravintolalla pitää olla nimi")
    
    searchname = name.lower()

    info = request.form["info"]
    if len(info) > 1000:
        render_template("error.html", message="Infossa saa korkeintaan olla 1000 merkkiä")

    if info=="":
        info="-"

    openinghours = request.form["openinghours"]
    if len(openinghours) > 100:
        render_template("error.html", message="Aukioloajassa saa korkeintaan olla 1000 merkkiä")

    if openinghours=="":
        openinghours="ei tietoa"
        
    address = request.form["address"]
    if len(address) > 100:
        render_template("error.html", message="Osoite saa korkeintaan olla 100 merkkiä")
        
    if address=="":
        "ei tietoa"

    restaurant_id = request.form["restaurant_id"]
    restaurants.update_restaurant(name, info, openinghours, address, users.user_id(), restaurant_id, searchname)
    return redirect("/restaurant/"+str(restaurant_id))

@app.route("/add_menu", methods=["post"])
def add_menu():
    users.check_csrf()
    name = request.form["name"]
    if len(name) > 25:
        render_template("error.html", message="Ruuan nimessä saa korkeintaan olla 25 merkkiä")
     
    if len(name) < 1:
        render_template("error.html", message="Rualla pitää olla nimi")
        
    price = request.form["price"]
    if len(price) > 1000:
        render_template("error.html", message="Hinnassa saa korkeintaan olla 1000 merkkiä")

    if len(price) < 1:
        render_template("error.html", message="Rualla pitää olla hinta")

    restaurant_id = request.form["restaurant_id"]
    restaurants.add_menu(name, price, restaurant_id)
    return redirect("/restaurant/"+str(restaurant_id))
