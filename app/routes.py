from flask import render_template, request, redirect, url_for, flash
from app.models import Author, Book, Borrow
from app import app, db
from app.forms2 import AuthorForm, BookForm, BorrowForm


@app.route('/authors/', methods=["GET", "POST"])
def authors_list():
    form = AuthorForm()
    authors = Author.query.all()
    authors_names = [author.name for author in authors]
    error = None
    if request.method == "POST":
        if not form.name.data in authors_names:
            name = form.data['name']
            author = Author(name=name)
            db.session.add(author)
            db.session.commit()
        else:
            error = "Taki autor już istnieje w bazie. Dodaj do nazwiska np. datę urodzenia, aby ich odróżnić"
            return render_template("authors.html", authors=authors, form=form, error=error)

        return redirect(url_for("authors_list"))

    return render_template("authors.html", authors=authors, form=form, error=error)


@app.route('/authors/<int:author_id>', methods=["GET", "POST"])
def author_books(author_id):
    author = Author.query.get(author_id)
    books = author.books
    all_titles = [book.title for book in Book.query.all()]
    form = BookForm()
    error = None
    if request.method == "POST":
        title = form.data['title']
        if title in all_titles:
            book = [book for book in Book.query.filter_by(title=title)][0]
            if author in book.authors:
                error = "Tak książka jest już przypisana do tego autora."
                return render_template("author.html",
                                       author=author, books=books, form=form, error=error)
            else:
                author.books.append(book)
                db.session.commit()
        else:
            book = Book(title=title)
            db.session.add(book)
            author.books.append(book)
            db.session.commit()

        return redirect(url_for('.author_books', author_id=author_id))

    return render_template("author.html",
                           author=author, books=books, form=form, error=error)


@app.route('/books/', methods=["GET", "POST"])
def books_list():
    form = BookForm()
    books = Book.query.all()
    authors_names = [author.name for author in Author.query.all()]
    error = None
    if request.method == "POST":
        title = form.data['title']
        authors = [form.data['author1'], form.data['author2'], form.data['author3']]
        if not title in [book.title for book in books]:
            book = Book(title=title)
            db.session.add(book)
            db.session.commit()
            for author in authors:
                if author=='':
                    pass
                elif author in authors_names:
                    for a in Author.query.filter_by(name=author):
                        if a.name == author:
                            book.authors.append(a)
                            db.session.commit()
                        else:
                            pass
                elif author not in authors_names:
                    author = Author(name=author)
                    book.authors.append(author)
                    db.session.commit()
        else:
            error = "Książka o tym tytule istnieje już w bazie. Jeśli to inna książka, " \
                    "dodaj szczegół, np. rok wydania, aby je odróżnić."
            return render_template("books.html", books=books, form=form, error=error)

        return redirect(url_for("books_list"))

    return render_template("books.html", books=books, form=form, error=error)


@app.route('/books/<int:book_id>', methods=["GET", "POST"])
def book_borrowings(book_id):
    error = None
    book = Book.query.get(book_id)
    borrows = [borrow for borrow in book.borrows]
    if len(borrows) != 0:
        latest = book.borrows[-1]
    else:
        latest = None
    form = BorrowForm()
    if request.method == "POST":
        if form.data['in_stock'] == "Wypożyczam":
            if (latest is None) or (latest.in_stock == True):
                borrow = Borrow(in_stock=False, book=book)
                db.session.add(borrow)
                db.session.commit()
            else:
                error = 'Nie możesz wypożyczyć tej książki'
                return render_template("book.html",
                                       book=book, form=form, borrows=borrows, error=error)

        elif form.data['in_stock'] == "Oddaję":
            if (latest is None) or (latest.in_stock == False):
                borrow = Borrow(in_stock=True, book=book)
                db.session.add(borrow)
                db.session.commit()
            else:
                error = 'Nie możesz oddać tej książki'
                return render_template("book.html",
                                       book=book, form=form, borrows=borrows, error=error)

        return redirect(url_for('.book_borrowings', book_id=book_id))

    return render_template("book.html",
                           book=book, form=form, borrows=borrows, error=error)
