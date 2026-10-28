import os

from flask import Flask, abort, render_template

app = Flask(__name__)

BOOKS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "books")


def list_books():
    """Book names (file names without the .txt extension)."""
    return sorted(
        os.path.splitext(f)[0] for f in os.listdir(BOOKS_DIR) if f.endswith(".txt")
    )


@app.route("/")
def index():
    return render_template("index.html", books=list_books())


# URL with a variable part: /book/The_Two_Towers
@app.route("/book/<book_name>")
def show_book(book_name):
    # Only allow names that match an existing book file (blocks path tricks)
    if book_name not in list_books():
        abort(404)

    path = os.path.join(BOOKS_DIR, book_name + ".txt")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Send title + content to the HTML template
    return render_template("book.html", title=book_name, content=content)


@app.errorhandler(404)
def not_found(_):
    return render_template("index.html", books=list_books(), error=True), 404


if __name__ == "__main__":
    app.run(debug=True)
