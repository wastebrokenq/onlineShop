from flask import Flask, render_template, redirect, url_for, request, session, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

# Инициализация Flask приложения
app = Flask(__name__)

# Конфигурация приложения
app.config['SECRET_KEY'] = 'lorsikponosik' # Секретный ключ для поддержания сессии
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///onlineShop.db' # Путь к базе данных
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Отключение отслеживания модификаций в SQLAlchemy
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30) # Временной интервал после которого сессия истекает

# Инициализация SQLAlchemy и LoginManager
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # Указывается представление, которое необходимо использовать для входа

# Описание моделей данных
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.username}>'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    description = db.Column(db.String(300))
    images = db.Column(db.Text) 

    def image_list(self):
        return self.images.split(',') if self.images else []
    
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    vk_link = db.Column(db.String(255))
    full_name = db.Column(db.String(200), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    comment = db.Column(db.Text)
    payment_method = db.Column(db.String(50), default='Кредитной картой')
    status = db.Column(db.String(100), default='pending')  # Например, 'pending', 'shipped', 'delivered'

    user = db.relationship('User', backref='orders')

    def __repr__(self):
        return f"<Order {self.id} by User {self.user_id}>"

# Кастомные представления для Admin интерфейса
class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

# Инициализация Admin интерфейса
admin = Admin(app, name='ProductAdmin', template_mode='bootstrap3', index_view=MyAdminIndexView())
admin.add_view(MyModelView(Product, db.session))

# Определение маршрутов и представлений
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

@app.route('/order')
def order():
    return render_template('order_form.html')

@app.route('/submit_order', methods=['POST'])
def submit_order():
    order = Order(
        email=request.form['email'],
        vk_link=request.form['vk_link'],
        full_name=request.form['full_name'],
        country=request.form['country'],
        address=request.form['address'],
        postal_code=request.form['postal_code'],
        phone_number=request.form['phone'],
        comment=request.form.get('comment', ''),  # используйте пустую строку как значение по умолчанию
        payment_method=request.form['payment_method']
    )
    db.session.add(order)
    db.session.commit()
    return 'Заказ получен'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('admin.index'))
        return 'Invalid username or password'
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()  # Удаление данных из сессии
    response = make_response(redirect(url_for('login')))
    response.set_cookie('session', '', expires=0)  # Удаление cookie
    return response

# Запуск приложения
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создание таблиц, если они еще не созданы
        if User.query.filter_by(username='admin').first() is None: # Создание администратора, если его нет
            hashed_password = generate_password_hash('d1letantoss676', method='pbkdf2:sha256')
            admin_user = User(username='admin', password=hashed_password, is_admin=True)
            db.session.add(admin_user)
            db.session.commit()

    app.run(debug=True) # Запуск приложения в режиме отладки