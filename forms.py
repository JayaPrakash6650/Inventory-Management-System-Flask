from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import InputRequired, AnyOf, NumberRange
from database import local_session, Product, Location

class Navigation_Form(FlaskForm):
    prod_nav = SubmitField("Product")
    loc_nav = SubmitField("Location")
    mov_nav = SubmitField("Movement")
 
class Product_Form(FlaskForm):
    name_prod = StringField(validators=[InputRequired()])
    qty_prod = IntegerField(validators=[InputRequired()])
    add_prod = SubmitField("Add")
    edit_prod = SubmitField("Edit")

class Location_Form(FlaskForm):
    name_loc = StringField(validators=[InputRequired()])
    add_loc = SubmitField("Add")
    edit_loc = SubmitField("Edit")

class Movement_Form(FlaskForm):
    location_list = [""]
    id_list = []
    for tuples in local_session.query(Location.location_name).all():
        for value in tuples:
            location_list.append(value)
    for tuples in local_session.query(Product.product_id).all():
        for value in tuples:
            id_list.append(value)
    from_loc = StringField(validators=[AnyOf(location_list)])
    to_loc = StringField(validators=[AnyOf(location_list)])
    prod_id_mov = IntegerField(validators=[AnyOf(id_list)])
    prod_qty_mov = IntegerField(validators=[InputRequired(), NumberRange(min=0)])
    add_mov = SubmitField("Add")
    edit_mov = SubmitField("Edit")