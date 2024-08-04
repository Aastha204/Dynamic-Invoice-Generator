from . import db
from flask_login import UserMixin
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(100), default="Name")
    city = db.Column(db.String(100), default="City")
    country = db.Column(db.String(100), default="Country")
    occupation = db.Column(db.String(100), default="Occupation")
    occupation_city = db.Column(db.String(100), default="Occupation City")
    occupation_country = db.Column(db.String(100), default="Occupation Country")
    invoices = db.relationship('Invoice', backref='user', lazy=True)
    subscriptions = db.relationship('Subscription', backref='user', lazy=True)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __str__(self):
        return f'<User {self.username}>'




class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    template_id = db.Column(db.Integer, nullable=False)
    invoice_generate_date = db.Column(db.Date, default=datetime.utcnow)

    receiver_name = db.Column(db.String(255), default="Receiver Name", nullable=True)
    receiver_email = db.Column(db.String(255), default="Receiver Email", nullable=True)
    receiver_phone = db.Column(db.String(20), default="Receiver Phone no", nullable=True)
    receiver_houseno = db.Column(db.String(20), default="Receiver House No", nullable=True)
    receiver_city = db.Column(db.String(20), default="Receiver city", nullable=True)
    receiver_country = db.Column(db.String(20), default="Receiver country", nullable=True)

    due_date = db.Column(db.String(20),nullable=False)
    amount = db.Column(db.Float, default=0.0, nullable=True)

    receiver_company_name = db.Column(db.String(255), default="Receiver Company Name", nullable=True)
    sender_company_name = db.Column(db.String(255), default="Sender Company Name", nullable=True)

    sender_houseno = db.Column(db.String(255), default="Sender House No", nullable=True)
    sender_city = db.Column(db.String(255), default="Sender City", nullable=True)
    sender_country = db.Column(db.String(255), default="Sender Country", nullable=True)
    sender_email = db.Column(db.String(255), default="Sender Email", nullable=True)
    sender_phone = db.Column(db.String(20), default="Sender Phone", nullable=True)

    discount = db.Column(db.Float, nullable=True)
    total_tax = db.Column(db.Float, nullable=True)
    sub_total = db.Column(db.Float, nullable=True)
    remarks = db.Column(db.Text, nullable=True)
    payment_instructions = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='draft')  # Indicates if the invoice is a draft or final
    Template1 = db.relationship('template_1', backref=db.backref('Invoice', lazy=True))
    Template2 = db.relationship('template_2_3', backref=db.backref('Invoice', lazy=True))

class template_2_3(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False)
    hours_worked1 = db.Column(db.Integer, default=0)
    description1 = db.Column(db.String(255), default="A")
    rate_per_hour1 = db.Column(db.Float, default=0.0)
    amount1 = db.Column(db.Float, default=0.0)
    hours_worked2 = db.Column(db.Integer, default=0)
    description2 = db.Column(db.String(255), default="B")
    rate_per_hour2 = db.Column(db.Float, default=0.0)
    amount2 = db.Column(db.Float, default=0.0)
    hours_worked3 = db.Column(db.Integer, default=0)
    description3 = db.Column(db.String(255), default="C")
    rate_per_hour3 = db.Column(db.Float, default=0.0)
    amount3 = db.Column(db.Float, default=0.0)


class template_1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False)
    description1 = db.Column(db.String(255), default="A", nullable=True)
    quantity1 = db.Column(db.Integer, default=0, nullable=True)
    amount1 = db.Column(db.Float, default=0.0, nullable=True)
    description2 = db.Column(db.String(255), default="A", nullable=True)
    quantity2 = db.Column(db.Integer, default=0, nullable=True)
    amount2 = db.Column(db.Float, default=0.0, nullable=True)
    description3 = db.Column(db.String(255), default="A", nullable=True)
    quantity3 = db.Column(db.Integer, default=0, nullable=True)
    amount3 = db.Column(db.Float, default=0.0, nullable=True)
    description4 = db.Column(db.String(255), default="A", nullable=True)
    quantity4 = db.Column(db.Integer, default=0, nullable=True)
    amount4 = db.Column(db.Float, default=0.0, nullable=True)
    description5 = db.Column(db.String(255), nullable=True)
    quantity5 = db.Column(db.Integer, nullable=True)
    amount5 = db.Column(db.Float, nullable=True)
    description6 = db.Column(db.String(255), nullable=True)
    quantity6 = db.Column(db.Integer, nullable=True)
    amount6 = db.Column(db.Float, nullable=True)


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(20), nullable=False)  # Freelancer, Enterprise, Contractor
    plan = db.Column(db.String(20), nullable=False)  # Monthly, Yearly
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"Subscription('{self.category}', '{self.plan}', '{self.start_date}', '{self.end_date}')"
