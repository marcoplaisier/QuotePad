import os
import random

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}/quotepad.db".format(os.getcwd())
    app.config['SECRET_KEY'] = str(random.getrandbits(60))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)

    return app


if __name__ == '__main__':
    from quotepad import interfaces

    app = create_app()
    interfaces.run()
