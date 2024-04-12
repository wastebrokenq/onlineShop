from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    products = [
        {'name': 'Кокоа (мягкая игрушка)', 'price': 1500, 'image': 'cocoa.jpg'},
        {'name': 'Игрушечный мишка', 'price': 1200, 'image': 'cocoa.jpg'},
        {'name': 'Игрушечный мишка', 'price': 1200, 'image': 'cocoa.jpg'},
        {'name': 'Игрушечный мишка', 'price': 1200, 'image': 'cocoa.jpg'},
        {'name': 'Игрушечный мишка', 'price': 1200, 'image': 'cocoa.jpg'},
        {'name': 'Плюшевый слон', 'price': 1800, 'image': 'cocoa.jpg'}
    ]
    return render_template("index.html", products=products)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contacts")
def contacts():
    return render_template("contacts.html")

if __name__ == '__main__':
    app.run(debug=True)