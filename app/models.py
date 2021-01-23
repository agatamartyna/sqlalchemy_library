from app import db
from datetime import datetime

association_table = db.Table('association_table', db.Model.metadata,
                             db.Column('book_id',
                                       db.Integer, db.ForeignKey('book.id')),
                             db.Column('author_id',
                                       db.Integer, db.ForeignKey('author.id'))
                             )


class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    books = db.relationship("Book",
                            secondary=association_table, lazy="subquery",
                            backref=db.backref('author', lazy=True))

    def __str__(self):
        return f"<Author {self.name}>"


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    authors = db.relationship("Author",
                              secondary=association_table,
                              lazy="subquery",
                              backref=db.backref('book', lazy=True))
    borrows = db.relationship("Borrow", backref="book", lazy="dynamic")

    def __str__(self):
        return f"<Book {self.title}>"


class Borrow(db.Model):
    __tablename__ = 'borrow'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    in_stock = db.Column(db.Boolean, unique=True, default=False)

    def __str__(self):
        return f"<Borrow {self.in_stock}>"
