import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail



db = SQLAlchemy()
mail = Mail()
DB_NAME = 'database.site'


def create_database():
    db.create_all()
    print('Database Created')


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hbnwdvbn ajnbsjn ahe'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    


    db.init_app(app)
    

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html')

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'routes.login'


    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    from .routes import routes
    from .admin import admin
    from .models import User, Invoice, Subscription,template_1,template_2_3

    app.register_blueprint(routes, url_prefix='/') 
    app.register_blueprint(admin, url_prefix='/') 
    # app.register_blueprint(admin, url_prefix='/')

    with app.app_context():
        create_database()

    return app

