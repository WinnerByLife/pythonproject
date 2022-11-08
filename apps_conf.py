from fastapi import FastAPI
from flask import Flask
from fastapi.middleware.wsgi import WSGIMiddleware
from flask_sqlalchemy import SQLAlchemy
from fastapi.staticfiles import StaticFiles
from database import engine
from product import models

from product.routers import router as products_routers
from user.routers import router as user_routers
import os

basedir = os.path.abspath(os.path.dirname(__file__))

flask_app_conf = Flask(__name__,
                       static_url_path='',
                       static_folder='static',
                       template_folder='templates',)

flask_app_conf.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')

flask_db = SQLAlchemy()

flask_app_conf.config['SECRET_KEY'] = 'my secret key'

flask_app_conf.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
flask_app_conf.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
flask_app_conf.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
flask_app_conf.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
flask_app_conf.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS')
flask_app_conf.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL')


with flask_app_conf.app_context():
    flask_db.init_app(flask_app_conf)


fastAPI_app_conf = FastAPI()

fastAPI_app_conf.mount("/store", WSGIMiddleware(flask_app_conf))
fastAPI_app_conf.include_router(products_routers)
fastAPI_app_conf.include_router(user_routers)
fastAPI_app_conf.mount("/static", StaticFiles(directory="static"), name="static")
models.Base.metadata.create_all(bind=engine)
