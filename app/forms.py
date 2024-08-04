from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, PasswordField, EmailField, BooleanField, SubmitField, SelectField, DateField, FormField, FieldList,  DecimalField
from wtforms.validators import DataRequired, length, NumberRange,Optional, Email
from flask_wtf.file import FileField, FileRequired
from flask_wtf import FlaskForm



class SignUpForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), length(min=2)])
    password1 = PasswordField('Enter Your Password', validators=[DataRequired(), length(min=6)])
    password2 = PasswordField('Confirm Your Password', validators=[DataRequired(), length(min=6)])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Enter Your Password', validators=[DataRequired()])
    submit = SubmitField('Log in')


class PasswordChangeForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired(), length(min=6)])
    new_password = PasswordField('New Password', validators=[DataRequired(), length(min=6)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), length(min=6)])
    change_password = SubmitField('Change Password')

class UserDetailChange(FlaskForm):
    name=StringField('Name', validators=[Optional(), length(min=2)])
    city=StringField('City', validators=[Optional(), length(min=2)])
    country=StringField('Country', validators=[Optional(), length(min=2)])
    occupation=StringField('Occupation', validators=[Optional(), length(min=2)])
    occupation_city=StringField('Occupation_city', validators=[Optional(), length(min=2)])
    occupation_country=StringField('Occupation_country', validators=[Optional(), length(min=2)])
    save_field = SubmitField('Save')


class InvoicedetailForm(FlaskForm):
    house_no = StringField('House No', validators=[Optional()])
    city = StringField('City', validators=[Optional()])
    country = StringField('Country', validators=[Optional()])
    email = StringField('Email', validators=[Optional(), Email()])
    phone_no = StringField('Phone No', validators=[Optional()])
    due_date = StringField('Due Date', validators=[Optional()])
    receiver_name = StringField('Receiver Name', validators=[Optional()])
    receiver_email = StringField('Receiver Email', validators=[DataRequired(), Email()])
    receiver_phone = StringField('Receiver Phone', validators=[Optional()])
    address_line1 = StringField('Address Line 1', validators=[Optional()])
    address_line2 = StringField('Address Line 2', validators=[Optional()])

    hours_worked1 = FloatField('Hours Worked 1', validators=[Optional()])
    description1 = StringField('Description 1', validators=[Optional()])
    rate_per_hour1 = FloatField('Rate per Hour 1', validators=[Optional()])
    amount1 = FloatField('Amount 1', validators=[Optional()])
    hours_worked2 = FloatField('Hours Worked 2', validators=[Optional()])
    description2 = StringField('Description 2', validators=[Optional()])
    rate_per_hour2 = FloatField('Rate per Hour 2', validators=[Optional()])
    amount2 = FloatField('Amount 2', validators=[Optional()])
    hours_worked3 = FloatField('Hours Worked 3', validators=[Optional()])
    description3 = StringField('Description 3', validators=[Optional()])
    rate_per_hour3 = FloatField('Rate per Hour 3', validators=[Optional()])
    amount3 = FloatField('Amount 3', validators=[Optional()])

    total_amount = FloatField('Total Amount', validators=[Optional()])
    gst = FloatField('GST', validators=[Optional()])
    grand_total = FloatField('Grand Total', validators=[Optional()])

    done = SubmitField('Done')


