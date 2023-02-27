import os
from flask_sqlalchemy import SQLAlchemy

from flask import Flask, render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bambetel.db'

db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("index.html", title="Головна")


if __name__ == "__main__":
    app.run(debug=True)
