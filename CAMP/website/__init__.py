from flask import Flask
from flask_mysqldb import MySQL


# Initialize MySQL connection
mysql = MySQL()

def create_app():  # Function to create a Flask application instance
    app = Flask(__name__)

    # Flask configuration settings
    app.config['SECRET_KEY'] = 'secret'  
    app.config['MYSQL_HOST'] = 'localhost'  
    app.config['MYSQL_USER'] = 'root'  
    app.config['MYSQL_PASSWORD'] = '1234'  
    app.config['MYSQL_DB'] = 'db_camp' 

    # Initialize MySQL database connection
    mysql.init_app(app)

    # Import blueprints for different app modules
    from .views import views
    from .auth import auth
    from .admin import admin
    from .student import student
    from .faculty import faculty

    # Register blueprints with Flask app
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')
    app.register_blueprint(student, url_prefix='/')
    app.register_blueprint(faculty, url_prefix='/')

    return app  # Return the Flask application instance
