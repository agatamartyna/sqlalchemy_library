from flask_wtf import FlaskForm
from wtforms import StringField, RadioField
from wtforms.validators import DataRequired


class AuthorForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])


class BookForm(FlaskForm):
    title = StringField("tytuł", validators=[DataRequired()])
    author1 = StringField("autor 1", validators=[DataRequired()])
    author2 = StringField("autor 2")
    author3 = StringField("autor 3")

class BorrowForm(FlaskForm):
    in_stock = RadioField("Status", choices = ["Wypożyczam", "Oddaję"],  validators=[DataRequired()])
