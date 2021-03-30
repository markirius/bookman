import os

from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = f"sqlite:///{os.path.join(project_dir,'bookdatabase.db')}"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"<Title: {self.title}>"


@app.route("/", methods=["GET", "POST"])
def home():
    books = None
    if request.form:
        try:
            book = Book(title=request.form.get("title"))
            db.session.add(book)
            db.session.commit()
            #print(request.form)
        except Exception as e:
            print(f"Failed to add this book: {book.title} - {e}")
    books = Book.query.all()
    return render_template("home.html", books=books)


@app.route("/update", methods=["POST"])
def update():
    try:
        new_title = request.form.get("newtitle")
        oldtitle = request.form.get("oldtitle")
        book = Book.query.filter_by(title=oldtitle).first()
        book.title = new_title
        db.session.commit()
    except Exception as e:
        print(f"Failed to update this book: {book.title} - {e}")
    return redirect("/")


@app.route("/delete/<id>", methods=["GET", "POST"])
def delete(id):
    try:
        book = Book.query.filter_by(id=id).first()
        db.session.delete(book)
        db.session.commit()
    except Exception as e:
        print(f"An error occurred during delete process: {e}")
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
