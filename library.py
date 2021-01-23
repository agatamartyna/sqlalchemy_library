from app import app, db
from app.models import Book, Author, Borrow, association_table

@app.shell_context_processor
def make_shell_context():
   return {
       "db": db,
       "Book": Book,
       "Author": Author,
       "Borrow": Borrow,
       "association_table": association_table
   }

if __name__ == "__main__":
    app.run(debug=True)
