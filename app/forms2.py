from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, BooleanField, SelectField
from wtforms.validators import DataRequired
from app.models import Author


class AuthorForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])


class BookForm(FlaskForm):
    title = StringField("tytuł", validators=[DataRequired()])
    author1 = SelectField("Autor 1")
    author2 = SelectField("Autor 2")
    author3 = SelectField("Autor 3")
    status = BooleanField("status", default=True)

    def __init__(self):
        super(BookForm, self).__init__()
        self.author1.choices = [''] +\
                               [author.name for author in Author.query.all()]
        self.author2.choices = [''] +\
                               [author.name for author in Author.query.all()]
        self.author3.choices = [''] +\
                               [author.name for author in Author.query.all()]


class BorrowForm(FlaskForm):
    in_stock = RadioField(
        "Status",
        choices=["Wypożyczam", "Oddaję"],
        validators=[DataRequired()]
    )
