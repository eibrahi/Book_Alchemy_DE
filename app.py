from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from data_models import db, Author, Book


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
db.init_app(app)

@app.route('/')
def hello_world():  # put application's code here
    return render_template('home.html')


#with app.app_context():
#   db.create_all()


if __name__ == '__main__':
    app.run()
