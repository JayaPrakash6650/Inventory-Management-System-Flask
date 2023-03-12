from flask import Flask, render_template, request, redirect, url_for
from database import local_session, Product, Location, Movement
from forms import Navigation_Form, Product_Form, Location_Form, Movement_Form


app = Flask(__name__)
app.config["SECRET_KEY"] = "A5implePa55word"


@app.route("/", methods=["POST", "GET"])
def nav_func():
    nav_form = Navigation_Form()
    if nav_form.validate_on_submit():
        if nav_form.prod_nav.data:
            return prod_func()
        elif nav_form.loc_nav.data:
            return loc_func()
        elif nav_form.mov_nav.data:
            return mov_func()
        elif nav_form.over_nav.data:
            return over_func()
    return render_template("index.html", nav_form=nav_form)

@app.route("/product", methods=["GET", "POST"])
def prod_func():
    nav_form = Navigation_Form()
    prod_form = Product_Form()
    all_product = local_session.query(Product).all()
    if prod_form.validate_on_submit():
        new_name_prod = prod_form.name_prod.data
        new_qty_prod = prod_form.qty_prod.data
        new_product = Product(product_name=new_name_prod, product_qty=new_qty_prod)
        try:
            local_session.add(new_product)
            local_session.commit()
        except:
            local_session.rollback()
    return render_template("products.html", nav_form=nav_form, prod_form=prod_form, products=all_product)

@app.route("/product/<type>/<int:id>", methods=["POST", "GET"])
def prod_edit_func(type, id):
    if type == "edit":
        prod_form = Product_Form()
        values = local_session.query(Product).all()
        return render_template("update.html", type="product", prod_form=prod_form, product=values[id-1])
    elif type == "update":
        prod_form = Product_Form()
        if prod_form.validate_on_submit():
            values = local_session.query(Product).all()
            values[id-1].product_name = prod_form.name_prod.data
            values[id-1].product_qty = prod_form.qty_prod.data
            try:
                local_session.commit()
            except:
                local_session.rollback()
    return redirect("/product")

@app.route("/location", methods=["GET", "POST"])
def loc_func():
    nav_form = Navigation_Form()
    loc_form = Location_Form()
    all_location = local_session.query(Location).all()
    if loc_form.validate_on_submit():
        new_name_loc = loc_form.name_loc.data
        new_location = Location(location_name=new_name_loc)
        try:
            local_session.add(new_location)
            local_session.commit()
        except:
            local_session.rollback()
    return render_template("locations.html", nav_form=nav_form, loc_form=loc_form, locations=all_location)

@app.route("/location/<type>/<int:id>", methods=["POST", "GET"])
def loc_edit_func(type, id):
    if type == "edit":
        loc_form = Location_Form()
        values = local_session.query(Location).all()
        return render_template("update.html", type="location", loc_form=loc_form, location=values[id-1])
    elif type == "update":
        loc_form = Location_Form()
        if loc_form.validate_on_submit():
            values = local_session.query(Location).all()
            values[id-1].location_name = loc_form.name_loc.data
            try:
                local_session.commit()
            except:
                local_session.rollback()
    return redirect("/location")

@app.route("/movement", methods=["GET", "POST"])
def mov_func():
    nav_form = Navigation_Form()
    mov_form = Movement_Form()
    all_movement = local_session.query(Movement).all()
    product_list = []
    location_list= [""]
    for product in local_session.query(Product.product_name).all():
        product_list.append(product.product_name)
    for location in local_session.query(Location.location_name).all():
        location_list.append(location.location_name)
    mov_form.prod_name_mov.choices = product_list
    mov_form.from_loc.choices = location_list
    mov_form.to_loc.choices = location_list
    if mov_form.validate_on_submit():
        if mov_form.from_loc.data != mov_form.to_loc.data:
            new_from_loc = mov_form.from_loc.data
            new_to_loc = mov_form.to_loc.data
            new_prod_name_mov = mov_form.prod_name_mov.data
            new_prod_qty_mov = mov_form.prod_qty_mov.data
            if local_session.query(Product.product_qty).filter(Product.product_name == new_prod_name_mov).scalar() >= new_prod_qty_mov:
                new_movement = Movement(from_location=new_from_loc, to_location=new_to_loc, product_name=new_prod_name_mov, product_qty=new_prod_qty_mov)
                try:
                    local_session.add(new_movement)
                    local_session.commit()
                except:
                    local_session.rollback()
    return render_template("movements.html", nav_form=nav_form, mov_form=mov_form, movements=all_movement)

@app.route("/movement/<type>/<int:id>", methods=["POST", "GET"])
def mov_edit_func(type, id):
    mov_form = Movement_Form()
    product_list = []
    location_list= [""]
    for product in local_session.query(Product.product_name).all():
        product_list.append(product.product_name)
    for location in local_session.query(Location.location_name).all():
        location_list.append(location.location_name)
    mov_form.prod_name_mov.choices = product_list
    mov_form.from_loc.choices = location_list
    mov_form.to_loc.choices = location_list
    if type == "edit":
        values = local_session.query(Movement).all()
        return render_template("update.html", type="movement", mov_form=mov_form, movement=values[id-1])
    elif type == "update":
        if mov_form.validate_on_submit():
            if mov_form.from_loc.data != mov_form.to_loc.data:
                if local_session.query(Product.product_qty).filter(Product.product_name == mov_form.prod_name_mov.data).scalar() >= mov_form.prod_qty_mov.data:
                    values = local_session.query(Movement).all()
                    values[id-1].from_location = mov_form.from_loc.data
                    values[id-1].to_location = mov_form.to_loc.data
                    values[id-1].product_name = mov_form.prod_name_mov.data
                    values[id-1].product_qty = mov_form.prod_qty_mov.data
                    try:
                        local_session.commit()
                    except:
                        local_session.rollback()
    return redirect("/movement")

@app.route("/overview")
def over_func():
    nav_form = Navigation_Form()
    return render_template("overview.html", nav_form=nav_form)


if __name__ == "__main__":
    app.run(debug=True)