from flask import Flask, render_template

app = Flask(__name__)

products = [
    {'name': 'Кокоа (мягкая игрушка)', 'price': 1500, 'images': ['cocoa.jpg']},
    {'name': 'Значки Комару, Кокоа и Комуги', 'price': 120, 'images': ['icons1.jpeg', 'icons2.jpeg']},
    {'name': 'Игрушечный мишка', 'price': 1200, 'images': ['cocoa.jpg']},
    {'name': 'Игрушечный мишка', 'price': 1200, 'images': ['cocoa.jpg']},
    {'name': 'Игрушечный мишка', 'price': 1200, 'images': ['cocoa.jpg']},
    {'name': 'Плюшевый слон', 'price': 1800, 'images': ['cocoa.jpg']}
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