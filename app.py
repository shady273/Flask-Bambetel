import os
import pprint
import time
import threading
from apscheduler.schedulers.background import BackgroundScheduler
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
from sqlalchemy import asc
from flask_paginate import Pagination, get_page_parameter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bambetel.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class AllCoins(db.Model):
    __tablename__ = 'all_coins'
    __table_args__ = {'extend_existing': True}
    rating = db.Column(db.Integer, primary_key=True)
    id_coin = db.Column(db.String, unique=True)
    symbol = db.Column(db.String)
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    pr = db.relationship("Profiles", backref="all_coins", uselist=False)


class Profiles(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    coin_id = db.Column(db.String, db.ForeignKey('all_coins.id_coin'), unique=True)
    cg_rank = db.Column(db.Integer)
    img_large = db.Column(db.String)
    img_small = db.Column(db.String)
    img_thumb = db.Column(db.String)
    homepage = db.Column(db.String)


def format_number(value):
    return "{:,}".format(value)


app.jinja_env.filters['format_number'] = format_number

scheduler = BackgroundScheduler()

lock = threading.Lock()


@scheduler.scheduled_job('interval', minutes=10)
def update_coin_price():
    with lock:
        from CoinGecko import updata_price
        start_time = time.time()
        updata_price()
        end_time = time.time()
        elapsed_time = end_time - start_time
        current_time = time.localtime()
        print(f"""Coin prise update: time {elapsed_time / 60} minutes
Current time: {current_time.tm_hour}:{current_time.tm_min}:{current_time.tm_sec}""")


@app.route("/")
def index():
    with app.app_context():
        page = request.args.get(get_page_parameter(), type=int, default=1)
        per_page = 20
        all_coins_data = db.session.query(AllCoins, Profiles). \
            join(Profiles, AllCoins.id_coin == Profiles.coin_id). \
            order_by(asc(AllCoins.rating)). \
            paginate(page=page, per_page=per_page)

        pagination = Pagination(page=page, total=all_coins_data.total, per_page=per_page, css_framework='bootstrap4')

    return render_template("index.html", title="Головна", all_coins_data=all_coins_data, pagination=pagination)


scheduler.start()
if __name__ == "__main__":
    app.run(debug=True)
