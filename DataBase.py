from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bambetel.db'
#
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
#
#
# class AllCoins(db.Model):
#     __table_args__ = {'extend_existing': True}
#     id = db.Column(db.Integer, primary_key=True)
#     rating = db.Column(db.Integer)
#     id_coin = db.Column(db.String, unique=True)
#     symbol = db.Column(db.String)
#     name = db.Column(db.String)
#
#
# class Profiles(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     coin_id = db.Column(db.String, db.ForeignKey('all_coins.id_coin'), unique=True)
#     cg_rank = db.Column(db.Integer)
#     img_large = db.Column(db.String)
#     img_small = db.Column(db.String)
#     img_thumb = db.Column(db.String)
#     homepage = db.Column(db.String)
