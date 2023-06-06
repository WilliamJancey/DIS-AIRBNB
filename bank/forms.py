from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms import DecimalRangeField, IntegerRangeField, SelectMultipleField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, InputRequired
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
    id = StringField('email', validators=[DataRequired(),Length(min=2, max=60)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class HostLoginForm(FlaskForm):
    id = IntegerField('hid', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class OverviewForm(FlaskForm):
    roomtype = SelectField('Roomtype'  , choices=[], validators=[DataRequired()])
    price = DecimalRangeField('Price')
    nights = IntegerRangeField('Nights', render_kw={'min':'1', 'max':'14'})
    area = SelectMultipleField('Area', choices=[], validators=[DataRequired()])
    loc = SelectMultipleField('Location', choices=[], validators=[DataRequired()])
    submit = SubmitField('Confirm')

class RentForm(FlaskForm):
    nights = IntegerField('Nights', validators=[InputRequired()])
    submit = SubmitField('Confirm')
    
class VisitForm(FlaskForm):
    attraction = SelectField('Attraction'  , choices=[], validators=[DataRequired()])
    loc = SelectField('Location'  , choices=[], validators=[DataRequired()])
    submit = SubmitField('Confirm')

class TransportationForm(FlaskForm):
    vehicle = SelectField('Vehicle'  , choices=[], validators=[DataRequired()])
    trips = IntegerField('Trips pr. day', validators=[DataRequired()])
    submit = SubmitField('Confirm')