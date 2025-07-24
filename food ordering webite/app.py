from flask import Flask, render_template, request, redirect, url_for, session, flash
import csv
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "replace_with_a_random_secret"

ORDER_FILE_PATH = "orders.txt"
MENU_CSV_PATH = "menu.csv"

def load_menu():
    menu = []
    with open(MENU_CSV_PATH) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) == 3:
                menu.append({
                    "name": row[0].strip(),
                    "price": float(row[1].strip()),
                    "img": row[2].strip()
                })
    return menu

def parse_orders_file():
    orders = []
    if not os.path.exists(ORDER_FILE_PATH):
        return orders  # no orders yet

    with open(ORDER_FILE_PATH, encoding="utf-8") as f:
        content = f.read()

    # Split orders by "--- Order at"
    raw_orders = content.split('--- Order at ')[1:]  # first split part before first order is empty
    for raw in raw_orders:
        lines = raw.strip().splitlines()
        order = {}
        # The first line contains timestamp plus rest of the line
        order['timestamp'] = lines[0].strip()
        details = []
        total = None
        for line in lines[1:]:
            if line.startswith('Table Number:'):
                order['table'] = line.replace('Table Number:', '').strip()
            elif line.startswith('Name:'):
                order['name'] = line.replace('Name:', '').strip()
            elif line.startswith('Mobile:'):
                order['mobile'] = line.replace('Mobile:', '').strip()
            elif line.startswith('Total:'):
                total_str = line.replace('Total:', '').strip()
                # Remove any rupees symbol and replace if present, parse as float
                order['total'] = total_str.replace('₹', '$')  # just replace symbol, keep amount
            elif line.startswith('---') or not line.strip():
                continue
            else:
                # line example: "Pizza x2 - ₹17.98"
                parts = line.rsplit(' - $', 1)  # switched to $ symbol here!
                if len(parts) != 2:
                    # fallback if the file still has ₹ symbol
                    parts = line.rsplit(' - ₹', 1)  
                if len(parts) == 2:
                    item_part, price_part = parts
                    if ' x' in item_part:
                        item_name, qty_str = item_part.rsplit(' x', 1)
                        details.append({
                            'item': item_name.strip(),
                            'qty': int(qty_str),
                            'price': float(price_part)
                        })
        order['details'] = details
        if not order.get('total'):
            order['total'] = 'N/A'
        orders.append(order)
    return orders


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        mobile = request.form.get("mobile", "").strip()
        if not name or not mobile.startswith('+') or len(mobile) < 10:
            flash("Enter valid name and mobile number including country code (e.g. +919999999999).", "danger")
        else:
            session["user"] = {"name": name, "mobile": mobile}
            return redirect(url_for("table_number"))
    return render_template("login.html")


@app.route("/table", methods=["GET", "POST"])
def table_number():
    if "user" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        table = request.form.get("table", "").strip()
        if not table.isdigit():
            flash("Invalid table number", "danger")
        else:
            session["table"] = table
            session["cart"] = {}
            return redirect(url_for("menu"))
    return render_template("table.html")


@app.route("/menu", methods=["GET", "POST"])
def menu():
    if "user" not in session or "table" not in session:
        return redirect(url_for("login"))
    menu = load_menu()
    cart = session.get("cart", {})
    if request.method == "POST":
        item_name = request.form.get("item")
        qty = int(request.form.get("qty", 1))
        if item_name:
            cart[item_name] = cart.get(item_name, 0) + qty
            session["cart"] = cart
            flash(f"Added {item_name} x{qty} to cart", "success")
            return redirect(url_for("menu"))
    return render_template("menu.html", menu=menu, cart=cart)


@app.route("/orders")
def orders():
    if "user" not in session or "table" not in session:
        return redirect(url_for("login"))

    orders = parse_orders_file()
    if not orders:
        return render_template("orders.html", orders=None)

    return render_template("orders.html", orders=orders)


@app.route("/cart", methods=["GET", "POST"])
def cart():
    if "user" not in session or "table" not in session:
        return redirect(url_for("login"))
    menu = load_menu()
    cart = session.get("cart", {})

    if request.method == "POST":
        if "remove" in request.form:
            item_to_remove = request.form.get("remove")
            if item_to_remove in cart:
                cart.pop(item_to_remove)
                session["cart"] = cart
                flash(f"Removed {item_to_remove} from cart.", "info")
            return redirect(url_for("cart"))
        elif "clear" in request.form:
            session["cart"] = {}
            return redirect(url_for("cart"))
        elif "update" in request.form:
            for item in list(cart.keys()):
                qty = int(request.form.get(f"qty_{item}", 0))
                if qty > 0:
                    cart[item] = qty
                else:
                    cart.pop(item)
            session["cart"] = cart
            flash("Cart updated.", "success")
            return redirect(url_for("cart"))
        elif "place_order" in request.form:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            table = session.get("table")
            user = session.get("user")
            menu_items = {m["name"]: m for m in menu}
            total = 0
            with open(ORDER_FILE_PATH, "a", encoding="utf-8") as f:
                f.write(f"--- Order at {timestamp} ---\n")
                f.write(f"Table Number: {table}\n")
                f.write(f"Name: {user['name']}\nMobile: {user['mobile']}\n")
                for item, qty in cart.items():
                    price = menu_items[item]["price"]
                    subtotal = price * qty
                    f.write(f"{item} x{qty} - ${subtotal:.2f}\n")
                    total += subtotal
                f.write(f"Total: ${total:.2f}\n")
                f.write('-' * 30 + '\n\n')
            session.pop("cart", None)
            flash("Order placed!", "success")
            return redirect(url_for("menu"))

    # Prepare cart data for display
    menu_items = {m["name"]: m for m in menu}
    cart_items = []
    total = 0
    for name, qty in cart.items():
        price = menu_items[name]["price"]
        subtotal = qty * price
        cart_items.append({"name": name, "img": menu_items[name]["img"], "qty": qty, "price": price, "subtotal": subtotal})
        total += subtotal
    return render_template("cart.html", cart_items=cart_items, total=total)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
