from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# creating database
db = SQLAlchemy()
DB_NAME = "database.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# creates Flask app and returns it
def create_app():
    app = Flask(__name__)   # first thing to do when making flask app
    app.config['SECRET_KEY'] = "helloworld"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # tells flask where DB is
    db.init_app(app) # initialize DB with our flask app
    
    # below is how to create flask route/endpoint
    # @app.route("/")
    # def home():
    #     return "<h1>Hello</h1>"
    
    # need . before file name for relative import
    # when inside python package
    from .views import views
    from .auth import auth
    
    # url_prefix must be before path in corresponding blueprint
    # when on website to access that view
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    
    # must import each model individually before creating DB
    from .models import User, Needle, Yarn
    
    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = "auth.login" # if user isn't logged in, shows login page
    login_manager.init_app(app)
    
    # login manager uses a session to determine if you are logged in or not
    # think of session as temp storage of user information at time of being on site
    # default time is 30 days
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def create_database(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app) # makes database file for us
        print("Created database!")