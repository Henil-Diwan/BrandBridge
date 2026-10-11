from flask import Flask
from extensions import db, migrate, bcrypt, jwt, cors, cache
from admin import setup_admin
from worker import celery_init_app
import flask_excel as excel
from routes import routes_bp
from celery.schedules import crontab
from tasks import daily_reminder, monthly_reminder

celery_app = None

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./project.db"
app.config["SECRET_KEY"] = "your_secret_key_here"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["API_BASE_URL"] = "http://localhost:5001"

app.config["CACHE_TYPE"] = "RedisCache"
app.config["CACHE_REDIS_HOST"] = "localhost"
app.config["CACHE_REDIS_PORT"] = 6379
app.config["CACHE_REDIS_DB"] = 3
app.config["CACHE_DEFAULT_TIMEOUT"] = 300

app.config["SMTP_SERVER"] = "localhost"
app.config["SMTP_PORT"] = 1025
app.config["SENDER_EMAIL"] = "Brandbridge@gmail.om"
app.config["SENDER_PASSWORD"] = "dummy_password"


db.init_app(app)
migrate.init_app(app, db)
bcrypt.init_app(app)
jwt.init_app(app)
cors.init_app(app)
cache.init_app(app)


setup_admin(app, db)

print("Celery app initialized.")


celery_app = celery_init_app(app)


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=0, minute=44),
        daily_reminder.s(),
    )
    sender.add_periodic_task(
        crontab(hour=22, minute=46),
        monthly_reminder.s(),
    )


app.register_blueprint(routes_bp)


if __name__ == "__main__":

    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
