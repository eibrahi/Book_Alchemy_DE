from operator import or_

import flask
from flask import Flask, render_template, request, redirect, flash
from data_models import db, Author, Book
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
db.init_app(app)


@app.route('/')
def home():
    """
    Zeigt die Startseite mit allen Büchern aus der Datenbank.
    """
    books = db.session.execute(db.select(Book)).scalars().all()
    return render_template('home.html', books=books)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """
    Löscht ein Buch anhand seiner ID aus der Datenbank.
    Nach erfolgreicher Löschung wird der Benutzer zur Startseite
    weitergeleitet und eine Erfolgsmeldung angezeigt.
    """

    book = db.session.execute(
        db.select(Book).where(Book.id == book_id)
    ).scalar_one_or_none()

    if not book:
        flash("Buch wurde nicht gefunden.")
        return redirect("/")

    author = book.author

    db.session.delete(book)
    db.session.commit()

    remaining_books = db.session.execute(
        db.select(Book).where(Book.author == author)
    ).scalars().all()

    if not remaining_books:
        db.session.delete(author)
        db.session.commit()

    flash("Buch erfolgreich gelöscht!")

    return redirect("/")

@app.route('/sort', methods=['GET'])
def sort():
    """
    Sortiert die Bücher nach Titel oder Autor.

    Die Sortierung wird über URL-Parameter gesteuert:
    - sort=title oder sort=author
    - direction=asc oder direction=desc
    """
    sort_by = request.args.get('sort', 'title')
    direction = request.args.get('direction', 'asc')

    if sort_by == 'title':
        if direction == 'asc':
            books = Book.query.order_by(Book.title.asc()).all()
        else:
            books = Book.query.order_by(Book.title.desc()).all()

    elif sort_by == 'author':
        if direction == 'asc':
            books = Book.query.join(Author).order_by(Author.name.asc()).all()
        else:
            books = Book.query.join(Author).order_by(Author.name.desc()).all()

    else:
        books = Book.query.all()

    return render_template('home.html', books=books)

@app.route('/search', methods=['GET'])
def search():
    """
    Durchsucht die Bücher nach dem eingegebenen Suchbegriff.
    Dabei werden sowohl der Buchtitel als auch der Name des Autors durchsucht.

    Gibt die gefundenen Bücher aus oder eine Meldung zurück,
    wenn keine passenden Bücher gefunden wurden.
    """
    query = request.args.get('query')

    books = db.session.execute(
        db.select(Book)
        .join(Book.author)
        .where(
            or_(Book.title.like(f'%{query}%'),
                 Author.name.like(f'%{query}%')
                )
        )
    ).scalars().all()

    if not books:
        return render_template(
            'home.html',
            books=[],
            massage=f"Keine Bücher für '{query} gefunden."
        )
    return render_template(
        'home.html',
        books=books,
    )



@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    Zeigt das Formular zum Anlegen eines Autors und
    speichert einen neuen Autor in der Datenbank.

    GET:
        Zeigt das Formular.

    POST:
        Liest die Formulardaten aus, erstellt einen Author
        und speichert ihn in der Datenbank.
    """
    if request.method == 'GET':
        return render_template('add_author.html')

    elif request.method == 'POST':

        name = request.form.get('name')
        birth_date = datetime.strptime(request.form['birthdate'], '%Y-%m-%d').date()
        date_of_death = request.form.get('date_of_death')

        if date_of_death:
            date_of_death = datetime.strptime(date_of_death, '%Y-%m-%d').date()
        else:
            date_of_death = None

        author = Author(
            name=name,
            birth_date=birth_date,
            date_of_death=date_of_death
        )

        db.session.add(author)
        db.session.commit()

    return "Author added successfully"


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    Zeigt das Formular zum Anlegen eines Buches und
    speichert ein neues Buch in der Datenbank.

    GET:
        Lädt alle Autoren und zeigt sie im Formular an.

    POST:
        Liest die Formulardaten aus, erstellt ein Book
        und speichert es in der Datenbank.
    """
    if request.method == 'GET':
        authors = db.session.execute(db.select(Author)).scalars().all()
        return render_template('add_book.html', authors=authors)

    elif request.method == 'POST':
        title = request.form.get('title')
        isbn = request.form.get('isbn')
        publication_year = int(request.form['publication_year'])
        author_id = int(request.form['author_id'])

        book = Book(
            title=title,
            isbn=isbn,
            publication_year=publication_year,
            author_id=author_id
        )

        db.session.add(book)
        db.session.commit()

    return "Book added successfully"


# with app.app_context():
#     db.create_all()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
