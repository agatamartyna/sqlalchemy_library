from flask import render_template, request, redirect, url_for
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
        # add new author
        if form.name.data not in authors_names:
            name = form.data['name']
            author = Author(name=name)
            db.session.add(author)
            db.session.commit()
        else:
            # Proviso for existing string:
            error = "Taki autor już istnieje w bazie. " \
                    "Dodaj do nazwiska np. datę urodzenia " \
                    "lub inicjał, aby ich odróżnić"
            return render_template("authors.html",
                                   authors=authors, form=form, error=error)

        return redirect(url_for("authors_list"))

    return render_template("authors.html",
                           authors=authors, form=form, error=error)


@app.route('/authors/<int:author_id>', methods=["GET", "POST"])
def author_books(author_id):
    author = Author.query.get(author_id)
    books = author.books
    all_titles = [book.title for book in Book.query.all()]
    form = BookForm()
    error = None
    if request.method == "POST":
        title = form.data['title']
        """An author does not typically write two books of the same title,
        if they do, they must be distinguished manually"""
        if title in all_titles:
            book = [book for book in Book.query.filter_by(title=title)][0]
            if author in book.authors:
                error = "Ta książka już istnieje w bazie."
                return render_template("author.html",
                                       author=author,
                                       books=books,
                                       form=form,
                                       error=error)
            # title exists, but the other author is missing
            else:
                author.books.append(book)
                db.session.commit()
        # most typical case: just enter some new title
        else:
            book = Book(title=title)
            """set default value for a new book on in_stock,
            there could be choice like in the /books/ routing
            (just to show you I can do it, enter a new book borrowed,
            which is silly) but have merci,
            I'm almost dead of this exi."""
            borrow = Borrow(in_stock=True, book=book)
            db.session.add(book)
            db.session.add(borrow)
            author.books.append(book)
            db.session.commit()

        return redirect(url_for('.author_books', author_id=author_id))

    return render_template("author.html",
                           author=author, books=books,
                           form=form, error=error)


@app.route('/books/', methods=["GET", "POST"])
def books_list():
    form = BookForm()
    books = Book.query.all()
    authors_names = [author.name for author in Author.query.all()]
    error = None
    if request.method == "POST":
        title = form.data['title']
        authors = [form.data['author1'], form.data['author2'],
                   form.data['author3']]
        # set default value for a new book on 'in_stock'
        status = form.data['status']
        if title not in [book.title for book in books]:
            book = Book(title=title)
            borrow = Borrow(in_stock=status, book=book)
            db.session.add(book)
            db.session.add(borrow)
            db.session.commit()
            for author in authors:
                if author == '':
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
            error = "Książka o tym tytule istnieje już w bazie. " \
                    "Jeśli to inna książka, dodaj szczegół, " \
                    "np. rok wydania, aby je odróżnić."
            return render_template("books.html", books=books,
                                   form=form, error=error)

        return redirect(url_for("books_list"))

    return render_template("books.html", books=books,
                           form=form, error=error)


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
            if (latest is None) or (latest.in_stock is True):
                borrow = Borrow(in_stock=False, book=book)
                db.session.add(borrow)
                db.session.commit()

            else:
                error = 'Nie możesz wypożyczyć tej książki'
                return render_template("book.html",
                                       book=book, form=form,
                                       borrows=borrows, error=error)

        elif form.data['in_stock'] == "Oddaję":
            if (latest is None) or (latest.in_stock is False):
                borrow = Borrow(in_stock=True, book=book)
                db.session.add(borrow)
                db.session.commit()
            else:
                error = 'Nie możesz oddać tej książki'
                return render_template("book.html",
                                       book=book, form=form,
                                       borrows=borrows, error=error)

        return redirect(url_for('.book_borrowings', book_id=book_id))

    return render_template("book.html",
                           book=book, form=form, borrows=borrows, error=error)
