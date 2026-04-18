from flask import Flask, render_template, request, redirect, session, url_for
from functools import wraps
from .auth import login_user
from .routes.products import products_bp
from .routes.customers import customers_bp
from .routes.inventory import inventory_bp
from .routes.orders import orders_bp
from .routes.routing import routing_bp
from .db import get_db_connection

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

app.secret_key = "your_secret_key_here"
app.register_blueprint(products_bp)
app.register_blueprint(customers_bp)
app.register_blueprint(inventory_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(routing_bp)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = login_user(
            request.form['username'],
            request.form['password']
        )

        if user_id:
            session['user_id'] = user_id
            session['username'] = request.form['username']
            return redirect('/')
        else:
            return "Invalid username or password"

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/products")
@login_required
def products_page():
    return render_template("products.html")

@app.route("/customers")
@login_required
def customers_page():
    return render_template("customers.html")

@app.route("/inventory")
@login_required
def inventory_page():
    return render_template("inventory.html")

@app.route("/production")
@login_required
def prduction_page():
    return render_template("production.html")

@app.route("/orders")
@login_required
def orders_page():
    return render_template("orders.html")

@app.route("/routing")
@login_required
def routing_page():
    return render_template("routing.html")

if __name__ == "__main__":
    app.run(debug=True)