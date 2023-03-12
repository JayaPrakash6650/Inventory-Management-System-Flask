from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import InputRequired, NumberRange 
from database import local_session, Product, Location


class Navigation_Form(FlaskForm):
    prod_nav = SubmitField("Product")
    loc_nav = SubmitField("Location")
    mov_nav = SubmitField("Movement")
    over_nav = SubmitField("Overview")
 
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
    from_loc = SelectField()
    to_loc = SelectField()
    prod_name_mov = SelectField()
    prod_qty_mov = IntegerField(validators=[InputRequired(), NumberRange(min=0)])
    add_mov = SubmitField("Add")
    edit_mov = SubmitField("Edit")