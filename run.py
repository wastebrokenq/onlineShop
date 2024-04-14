from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    description = db.Column(db.String(300))
    images = db.Column(db.Text) 

    def image_list(self):
        return self.images.split(',') if self.images else []

with app.app_context():
    db.create_all()

admin = Admin(app, name='ProductAdmin', template_mode='bootstrap3')
admin.add_view(ModelView(Product, db.session))

@app.route("/")
@app.route("/index")
def index():
    products = Product.query.all()
    return render_template("index.html", products=products)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/product/<int:product_id>")
def product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template("card.html", product=product)

if __name__ == '__main__':
    app.run(debug=True)
