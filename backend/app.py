from flask import Flask
from extensions import db, migrate, bcrypt, jwt, cors
from admin import setup_admin
from worker import celery_init_app
import flask_excel as excel
from routes import routes_bp 

celery_app = None

def create_app():
    global celery_app
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///./project.db'
    app.config["SECRET_KEY"] = 'your_secret_key_here'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["UPLOAD_FOLDER"] = 'uploads'
    app.config["API_BASE_URL"] = 'http://localhost:5001'

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    excel.init_excel

    # Setup admin panel
    setup_admin(app, db)

    


    # Initialize Celery
    celery_app = celery_init_app(app)

    # Register routes (importing here inside the factory) # Import routes only inside the factory
    app.register_blueprint(routes_bp)
    return app

# This part is required to run the app directly
if __name__ == '__main__':
    app = create_app()  # Create the app here, when running directly
    with app.app_context():
        db.create_all()  # Or whatever else needs to be done on app start
    app.run(debug=True, port=5001)
