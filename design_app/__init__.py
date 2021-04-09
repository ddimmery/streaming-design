from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis


app = Flask(__name__, instance_relative_config=False)
app.config.from_object('config.Config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
redis = FlaskRedis(app)

with app.app_context():
    import design_app.routes  # noqa: F401

    db.create_all()
