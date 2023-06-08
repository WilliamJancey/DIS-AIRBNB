from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms import DecimalRangeField, IntegerRangeField, SelectMultipleField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, InputRequired
from psycopg2 import sql
from bank import conn
class AddUserForm(FlaskForm):
    username = StringField('name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    CPR_number = IntegerField('uid',
                        validators=[DataRequired()])
    email = StringField('email',
                        validators=[DataRequired(), Length(min=2, max=60)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Add')


class UserLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Length(min=2, max=60)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class HostLoginForm(FlaskForm):
    id = IntegerField('hid', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

cur = conn.cursor()
areasql = sql.SQL("""SELECT DISTINCT area FROM Listings ORDER BY area""")
cur.execute(areasql)
areasql = cur.fetchall()
areachoices = [(area[0], area[0]) for area in areasql]
areachoices.insert(0, ('None','None'))
locsql = sql.SQL("""SELECT DISTINCT loc FROM Listings ORDER BY loc""")
cur.execute(locsql)
locsql = cur.fetchall()
locchoices = [(loc[0], loc[0]) for loc in locsql]
locchoices.insert(0, ('None','None'))
roomsql = sql.SQL("""SELECT DISTINCT room_type FROM Listings""")
cur.execute(roomsql)
roomsql = cur.fetchall()
roomchoices = [(room[0], room[0]) for room in roomsql]
roomchoices.insert(0, ('None','None'))


class OverviewForm(FlaskForm):
    room_type = SelectField('Roomtype'  , choices=roomchoices, validators=[DataRequired()])
    minprice = IntegerField('Price', default=0, render_kw={'min':'0', 'max':'10000'} )
    maxprice = IntegerField('Maxprice', default=10000, render_kw={'min':'0', 'max':'10000'} )
    nights = IntegerRangeField('Nights', render_kw={'min':'1', 'max':'14'})
    area = SelectField('Area', choices=areachoices, validators=[DataRequired()])
    loc = SelectField('Location', choices=locchoices, validators=[DataRequired()])
    submit = SubmitField('Confirm')

class RentForm(FlaskForm):
    nights = IntegerField('Nights', validators=[InputRequired()])
    submit = SubmitField('Confirm')
    
class VisitForm(FlaskForm):
    attraction = SelectField('Attraction'  , choices=[], validators=[DataRequired()])
    loc = SelectField('Location'  , choices=[], validators=[DataRequired()])
    submit = SubmitField('Confirm')

vehsql = sql.SQL("""SELECT DISTINCT vehicle FROM Transportation ORDER BY vehicle""")
cur.execute(vehsql)
vehsql = cur.fetchall()
vehchoices = [(veh[0], veh[0]) for veh in vehsql]
vehchoices.insert(0, ('None','None'))

class TransportationForm(FlaskForm):
    vehicle = SelectField('Vehicle'  , choices=vehchoices, validators=[InputRequired()])
    trips = IntegerField('Trips pr. day', validators=[InputRequired()])
    submit = SubmitField('Confirm')