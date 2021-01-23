from flask import render_template, request, redirect, url_for
from app.models import Author, Book
from app import app, db
from app.forms2 import AuthorForm, BookForm


@app.route('/authors/', methods=["GET", "POST"])
def authors_list():
    form = AuthorForm()
    authors = Author.query.all()
    if request.method == "POST":
        name = form.data['name']
        author = Author(name=name)
        db.session.add(author)
        db.session.commit()

        return redirect(url_for("authors_list"))

    return render_template("authors.html", authors=authors, form=form)


@app.route('/authors/<int:author_id>', methods=["GET", "POST"])
def author_books(author_id):
    author = Author.query.get(author_id)
    books = list(author.books)
    form = BookForm()
    if request.method == "POST":
        title = form.data['title']
        flag=0
        for book in Book.query.all():
            if book.title == title:
                author.books.append(book)
                db.session.commit()
                flag=1
                break
            else:
                continue
        if flag == 0:
            book = Book(title=title)
            db.session.add(book)
            author.books.append(book)
            db.session.commit()


        return redirect(url_for('.author_books', author_id=author_id))

    return render_template("author.html", author=author, books=books, form=form)











