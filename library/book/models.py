from django.db import models
from author.models import Author

class Book(models.Model):
    """
    This class represents a Book.
    """

    name = models.CharField(max_length=128,  default='Unknown')
    description = models.TextField()
    count = models.IntegerField(default=10)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        """
        Magic method is redefined to show all information about Book.
        """
        authors = ', '.join([author.name for author in self.authors.all()])
        return f"{self.id}: {self.name} - {self.description[:50]}... - {self.count} copies - Authors: {authors}"

    def __repr__(self):
        """
        This magic method is redefined to show class and id of Book object.
        """
        return f"<Book (id={self.id}, name={self.name}, count={self.count})>"

    @staticmethod
    def get_by_id(book_id):
        """
        Get book by ID.
        """
        return Book.objects.filter(id=book_id).first()

    @staticmethod
    def delete_by_id(book_id):
        """
        Deletes a book by ID.
        """
        book = Book.get_by_id(book_id)
        if book:
            book.delete()
            return True
        return False

    @staticmethod
    def create(name, description, count=10, authors=None):
        """
        Creates a new book.
        """
        book = Book(name=name, description=description, count=count)
        book.save()
        if authors:
            book.authors.set(authors)
        return book

    def to_dict(self):
        """
        Returns book data as a dictionary.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "count": self.count,
            "authors": [author.to_dict() for author in self.authors.all()],
        }

    def update(self, name=None, description=None, count=None):
        """
        Updates book in the database with the specified parameters.
        """
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if count is not None:
            self.count = count
        self.save()

    def add_authors(self, authors):
        """
        Add authors to book.
        """
        self.authors.add(*authors)

    def remove_authors(self, authors):
        """
        Remove authors from book.
        """
        self.authors.remove(*authors)

    @staticmethod
    def get_all():
        """
        Returns a QuerySet of all books.
        """
        return Book.objects.all()
