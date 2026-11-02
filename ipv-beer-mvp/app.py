from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path
from datetime import date

app = Flask(__name__)
app.secret_key = "ipv-beer-mvp-local"
DB_PATH = Path(__file__).with_name("ipvbeer.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            address TEXT
        );
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            product TEXT NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity > 0),
            unit_price REAL NOT NULL CHECK(unit_price >= 0),
            status TEXT NOT NULL DEFAULT 'Pendente',
            created_at TEXT NOT NULL,
            FOREIGN KEY(customer_id) REFERENCES customers(id)
        );
        """)
        db.commit()

@app.route("/")
def index():
    with get_db() as db:
        customers = db.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
        orders = db.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
        pending = db.execute("SELECT COUNT(*) FROM orders WHERE status = 'Pendente'").fetchone()[0]
        total = db.execute("SELECT COALESCE(SUM(quantity * unit_price), 0) FROM orders WHERE status = 'Entregue'").fetchone()[0]
        latest = db.execute("""
            SELECT orders.*, customers.name AS customer_name
            FROM orders JOIN customers ON customers.id = orders.customer_id
            ORDER BY orders.id DESC LIMIT 5
        """).fetchall()
    return render_template("index.html", customers=customers, orders=orders,
                           pending=pending, total=total, latest=latest)

@app.route("/clientes", methods=["GET", "POST"])
def customers():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()
        if not name or not phone:
            flash("Informe o nome e o telefone do cliente.", "error")
        else:
            with get_db() as db:
                db.execute("INSERT INTO customers (name, phone, address) VALUES (?, ?, ?)",
                           (name, phone, address))
                db.commit()
            flash("Cliente cadastrado com sucesso.", "success")
        return redirect(url_for("customers"))
    with get_db() as db:
        rows = db.execute("SELECT * FROM customers ORDER BY name").fetchall()
    return render_template("customers.html", customers=rows)

@app.route("/pedidos", methods=["GET", "POST"])
def orders():
    if request.method == "POST":
        customer_id = request.form.get("customer_id", type=int)
        product = request.form.get("product", "").strip()
        quantity = request.form.get("quantity", type=int)
        unit_price = request.form.get("unit_price", type=float)
        if not customer_id or not product or not quantity or quantity < 1 or unit_price is None or unit_price < 0:
            flash("Confira os dados do pedido e tente novamente.", "error")
        else:
            with get_db() as db:
                custumer = db.execute(
                    "SELECT id FROM customers WHERE id = ? , (customer_id,)
                ).fetchone()

                if customer is none:
                    flash("selecione um cliente cadastrado.", "error")
                else:
                    db.execute("""INSERT INTO orders
                        (customer_id, product, quantity, unit_price, status, created_at)
                        VALUES (?, ?, ?, ?, 'Pendente', ?)""",
                        (customer_id, product, quantity, unit_price, date.today().isoformat()))
                    db.commit()
                    flash("Pedido registrado com sucesso.", "success")
        return redirect(url_for("orders"))
    with get_db() as db:
        customers_list = db.execute("SELECT * FROM customers ORDER BY name").fetchall()
        rows = db.execute("""
            SELECT orders.*, customers.name AS customer_name
            FROM orders JOIN customers ON customers.id = orders.customer_id
            ORDER BY orders.id DESC
        """).fetchall()
    return render_template("orders.html", customers=customers_list, orders=rows)

@app.post("/pedido/<int:order_id>/status")
def update_status(order_id):
    status = request.form.get("status")
    if status not in ("Pendente", "Em entrega", "Entregue", "Cancelado"):
        flash("Status inválido.", "error")
    else:
        with get_db() as db:
            db.execute("UPDATE orders SET status = ? WHERE id = ?", (status, order_id))
            db.commit()
        flash("Status do pedido atualizado.", "success")
    return redirect(url_for("orders"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
