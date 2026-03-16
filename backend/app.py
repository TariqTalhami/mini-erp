from flask import Flask, render_template
from .routes.products import products_bp
from .routes.customers import customers_bp
from .db import get_db_connection

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static")

app.register_blueprint(products_bp)
app.register_blueprint(customers_bp)

@app.route("/test-db")
def test_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        result = cur.fetchone()
        conn.close()
        return f"Database OK: {result}"
    except Exception as e:
        return f"Database ERROR: {e}"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/products")
def products_page():
    return render_template("products.html")

@app.route("/customers")
def customers_page():
    return render_template("customers.html")

@app.route("/production")
def prduction_page():
    return render_template("production.html")

@app.route("/orders")
def orders_page():
    return render_template("orders.html")

if __name__ == "__main__":
    app.run(debug=True)