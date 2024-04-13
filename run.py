from flask import Flask, render_template

app = Flask(__name__)

products = [
    {'name': 'Кокоа (мягкая игрушка)', 'price': 1500, 'description': '', 'images': ['cocoa.jpg']},
    {'name': 'Значки Комару, Кокоа и Комуги', 'price': 120, 'description': 'Размер: 3.7*3.7 см. Цена указана за один значок.', 'images': ['icons1.jpeg', 'icons2.jpeg']},
    {'name': 'Патч Wide Cocoa (велкро)', 'price': 650, 'description': 'Размер: 7*5 см.', 'images': ['patch.jpg', 'patch_cocoa.jpg']},
    {'name': 'Вязаная Кокоа (брелочек)', 'price': 450, 'description': '', 'images': ['keychain_cocoa.jpg', 'keychain_cocoa2.jpg', 'keychain_cocoa3.jpg']},
]

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", products=products)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/product/<int:index>")
def product(index):
    product = products[index]
    return render_template("card.html", product=product)
   

if __name__ == '__main__':
    app.run(debug=True)