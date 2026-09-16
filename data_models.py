from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    birth_date = db.Column(db.Date)
    date_of_death = db.Column(db.Date)

    def __repr__(self):
        return '<Author %r>' '<Birth date %r>' % (
            self.name,
            self.birth_date
        )

    def __str__(self):
        return '<Author %r>' '<Birth date %r>' % (
            self.name,
            self.birth_date
        )


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String)
    title = db.Column(db.String)
    publication_year = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    author = db.relationship('Author', backref='books')

    def __repr__(self):
        return '<Book ISBN%r>' '<Book Title%r>' '<Author %r>' '<Book Publication Year%r>' % (
            self.isbn,
            self.title,
            self.author.name,
            self.publication_year
        )

    def __str__(self):
        return '<Book ISBN%r>' '<Book Title%r>' '<Author %r>' '<Book Publication Year%r>' % (
            self.isbn,
            self.title,
            self.author.name,
            self.publication_year
        )
