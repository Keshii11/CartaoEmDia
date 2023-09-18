from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
import pytz
from dateutil.relativedelta import relativedelta


# Configure app
app = Flask(__name__)

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure database
db = SQL("sqlite:///users_data.db")


# Set date
# Set the time zone to Brasília Time
brazil_time_zone = pytz.timezone('America/Sao_Paulo')
# Get the current date and time in the Brazil time zone
current_date_time_brazil = datetime.datetime.now(brazil_time_zone)
date_now = current_date_time_brazil.date()
day_now = date_now.day
month_now = date_now.month
year_now = date_now.year


@app.route("/add_invoice", methods=["POST", "GET"])
def add_invoice():
    if request.method == "POST":
        if not request.form.get("invoice"):
            flash("Dia inválido", "error")
            return redirect("/add_invoice")

        db.execute("UPDATE users SET invoice_day = ? WHERE id = ?", int(request.form.get("invoice")), session.get("user_id"))
        session["invoice"] = int(request.form.get("invoice"))
        return redirect("/")

    elif session.get("invoice") == -1:
        return render_template("index.html", invoice=session.get("invoice"))


    return redirect("/")


@app.route("/<string:date>")
def expenses_by_month(date):
    invoice_due = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    first_day = invoice_due - relativedelta(months=1)
    first_day += relativedelta(days=1)

    expenses = db.execute("SELECT id, date, name, installments, total, (total / installments) AS value FROM expenses WHERE user_id = ?", session.get("user_id"))

    month_expenses = []
    sum_value = 0

    for expense in expenses:
        expense_date = datetime.datetime.strptime(expense["date"], "%Y-%m-%d").date()
        for i in range(expense["installments"]):
            if first_day <= expense_date <= invoice_due:
                expense["date_format"] = '/'.join(reversed(expense["date"].split('-')))
                expense["installments_format"] = "{}/{}".format(i+1, expense["installments"])
                sum_value += expense["value"]
                month_expenses.append(expense)

            expense_date += relativedelta(months=1)

    return render_template("index.html", expenses=month_expenses, month=invoice_due.month, year=invoice_due.year, invoice=session.get("invoice"), first=first_day.strftime('%d/%m/%Y'), last=invoice_due.strftime('%d/%m/%Y'), sum_value=sum_value)

@app.route("/", methods=["POST", "GET"])
def index():
    # If don't find a cached user_id
    if not session.get("user_id"):
        return redirect("/login")

    return redirect("/{}-{}-{}".format(year_now, month_now, session.get("invoice")))

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST
    if request.method == "POST":
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Check username
        if len(rows) != 1 or not request.form.get("username"):
            return render_template("login.html", username_invalid=True)

        # Check password
        elif not request.form.get("password") or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html", password_invalid=True)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Set invoice
        session["invoice"] = rows[0]["invoice_day"]

        # Redirect user to home page
        return redirect("/add_invoice")

    # User reached route via GET
    else:
        return render_template("login.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    """register user"""
    # User reached route via POST
    if request.method == "POST":
        # Check username
        if not request.form.get("username"):
            return render_template("register.html", username_invalid=True)

        elif db.execute("SELECT username FROM users WHERE username = ?", request.form.get("username")):
            return render_template("register.html", username_exists=True)

        # Check password
        elif not request.form.get("password"):
            return render_template("register.html", password_invalid=True)

        elif request.form.get("password") != request.form.get("confirm"):
            return render_template("register.html", confirmation_invalid=True)

        # Create user
        else:
            # Insert user in db
            hash = generate_password_hash(request.form.get("password"))
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), hash)

            # Define user session
            rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
            session["user_id"] = rows[0]["id"]

            # Set invoice
            session["invoice"] = rows[0]["invoice_day"]

            return redirect("/add_invoice")

    # User reached route via GET
    else:
        return render_template("register.html")


@app.route("/add_items", methods=["POST", "GET"])
def add_items():
    # User reached route via POST
    if request.method == "POST":
        if not request.form.get("date"):
            flash("Data inválida", "error")
            return redirect("/")

        elif not request.form.get("name"):
            flash("Nome inválido", "error")
            return redirect("/")

        elif not request.form.get("value"):
            flash("Valor inválido", "error")
            return redirect("/")

        elif not request.form.get("installments"):
            flash("Parcelas inválida", "error")
            return redirect("/")

        else:
            # Set variables
            date = datetime.datetime.strptime(request.form.get("date"), "%Y-%m-%d").date()
            name = request.form.get("name")
            value = float(request.form.get("value"))
            installments = int(request.form.get("installments"))

            db.execute("INSERT INTO expenses (user_id, date, name, installments, total) VALUES (?, ?, ?, ?, ?)", session.get("user_id"), date, name, installments, value)

            return redirect("/")

    # User reached route via GET
    else:
        return redirect("/")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/previous/<string:date>")
def previous(date):
    """ Pagination button before"""
    date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    date -= relativedelta(months=1)

    return redirect("/{}".format(date))

@app.route("/next/<string:date>")
def next(date):
    """ Pagination button before"""
    date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    date += relativedelta(months=1)

    return redirect("/{}".format(date))


@app.route("/edit", methods=["POST", "GET"])
def edit():
    # User reached route via POST
    if request.method == "POST":
        if not request.form.get("date"):
            flash("Data inválida", "error")
            return redirect("/")

        elif not request.form.get("name"):
            flash("Nome inválido", "error")
            return redirect("/")

        elif not request.form.get("value"):
            flash("Valor inválido", "error")
            return redirect("/")

        elif not request.form.get("installments"):
            flash("Parcelas inválida", "error")
            return redirect("/")

        else:
            # Set variables
            date = datetime.datetime.strptime(request.form.get("date"), "%Y-%m-%d").date()
            name = request.form.get("name")
            value = float(request.form.get("value"))
            installments = int(request.form.get("installments"))
            id = int(request.form.get("id"))

            # Edit item
            db.execute("UPDATE expenses SET date = ?, name = ?, installments = ?, total = ? WHERE id = ?", date, name, installments, value, id)
            flash("Item editado", "success")

            return redirect("/")

    # User reached route via GET
    else:
        return redirect("/")

@app.route("/remove", methods=["POST", "GET"])
def remove():
    # User reached route via POST
    if request.method == "POST":
        # Delete item
        db.execute("DELETE FROM expenses WHERE id = ?", int(request.form.get("id")))
        flash("Item excluido", "success")

        return redirect("/")

    # User reached route via GET
    else:
        return redirect("/")
