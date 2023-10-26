# # __init__.py

# from flask import Flask
# from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy
# from app.blockchain import Blockchain
# from flask_login import LoginManager
# # from app.EHM_RECORD import EHM_RECORD

# app = Flask(__name__)
# app.debug = True

# app.config['SECRET_KEY'] = 'Ayodeji-1212'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fehr_database.db'



# db = SQLAlchemy(app)

# migrate = Migrate(app, db)
# blockchain = Blockchain()  # Initialize the blockchain
# login_manager = LoginManager(app)
# from app.models import User

# # Import your models and routes
# from app import routes
# # from app.routes import EHM_RECORD  # Replace with your actual blueprint

# # app.register_blueprint(EHM_RECORD, url_prefix='/ehr')  # Use a URL prefix for your Blueprint, e.g., '/ehr'
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))
import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.blockchain import Blockchain
from flask_login import LoginManager

app = Flask(__name__)
app.debug = True

# Use environment variables for configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY','Ayodeji-1212')

# Check if the application is running in a production environment (e.g., on Render)
if os.environ.get('FLASK_ENV') == 'production':
    # Set the database URI from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('sqlite:///famouzcoder_ehr_database.db')
else:
    # Set the database URI for local development
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///famouzehr_database.db'

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('sqlite:///famouzcoder_ehr_database.db')

# Initialize the SQLAlchemy database with your app
db = SQLAlchemy(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Initialize the blockchain
blockchain = Blockchain()

# Initialize Flask-Login and define the user loader function
login_manager = LoginManager(app)

from app.models import User

# Import your models and routes
from app import routes

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
