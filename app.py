from flask import Flask, render_template, request, redirect, session
from models import db, User, QueryLog
from config import Config
from detector import is_sql_safe
from werkzeug.security import generate_password_hash, check_password_hash


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Create database tables
    with app.app_context():
        db.create_all()

    # ---------------- ROUTES ------------------

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]

            if User.query.filter_by(email=email).first():
                return render_template("signup.html", error="Email already exists.")

            hashed = generate_password_hash(password)
            user = User(email=email, password=hashed)
            db.session.add(user)
            db.session.commit()

            return redirect("/login")

        return render_template("signup.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]

            user = User.query.filter_by(email=email).first()

            if not user or not check_password_hash(user.password, password):
                return render_template("login.html", error="Invalid email or password.")

            session["user_id"] = user.id
            return redirect("/admin")

        return render_template("login.html")

    @app.route("/admin", methods=["GET", "POST"])
    def admin():
        if "user_id" not in session:
            return redirect("/login")

        result = None
        query_text = ""

        if request.method == "POST":
            query_text = request.form["query"]
            result = "SAFE" if is_sql_safe(query_text) else "UNSAFE"

            log = QueryLog(query_text=query_text, result=result)
            db.session.add(log)
            db.session.commit()

        return render_template("admin.html", result=result, query_text=query_text)

    @app.route("/clear")
    def clear():
        return redirect("/admin")

    @app.route("/stats")
    def stats():
        if "user_id" not in session:
            return redirect("/login")

        # FIXED — inside function
        total = QueryLog.query.count()
        safe = QueryLog.query.filter_by(result="SAFE").count()
        unsafe = QueryLog.query.filter_by(result="UNSAFE").count()

        return render_template("stats.html", total=total, safe=safe, unsafe=unsafe)

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect("/login")

    return app


if __name__ == "__main__":
    import os
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
