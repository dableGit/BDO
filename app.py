from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, index=True)
    name = db.Column(db.String(64), index=True)
    market_main_category = db.Column(db.Integer, index=False)
    sub_main_category = db.Column(db.Integer, index=False)
    grade_type = db.Column(db.Integer, index=False)
    hardcap_min = db.Column(db.Integer, index=False)
    hardcap_max = db.Column(db.Integer, index=False)


class Market(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, index=False)
    date = db.Column(db.DateTime, index=False)
    price = db.Column(db.Integer, index=False)
    in_stock = db.Column(db.Integer, index=False)
    total_trades = db.Column(db.Integer, index=False)



with app.app_context():
    db.create_all()


@app.route('/')
def index():
    items = Item.query
    return render_template('bootstrap_table.html', title='Bootstrap Table', items=items)


if __name__ == '__main__':
    app.run()