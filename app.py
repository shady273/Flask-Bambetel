import os
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bambetel.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class AllCoins(db.Model):
    __table_args__ = {'extend_existing': True}
    rating = db.Column(db.Integer, primary_key=True)
    id_coin = db.Column(db.String, unique=True)
    symbol = db.Column(db.String)
    name = db.Column(db.String)


class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coin_id = db.Column(db.String, db.ForeignKey('all_coins.id_coin'), unique=True)
    cg_rank = db.Column(db.Integer)
    img_large = db.Column(db.String)
    img_small = db.Column(db.String)
    img_thumb = db.Column(db.String)
    homepage = db.Column(db.String)


@app.route("/")
def index():
    return render_template("index.html", title="Головна")


if __name__ == "__main__":
    app.run(debug=True)
