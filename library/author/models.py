from django.db import models


class Author(models.Model):
    """
    This class represents an Author.
    """

    name = models.CharField(max_length=20,  default='Unknown')
    surname = models.CharField(max_length=20,  default='Unknown')
    patronymic = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        """
        Magic method is redefined to show all information about Author.
        """
        return f"{self.id}: {self.name} {self.patronymic or ''} {self.surname}"

    def __repr__(self):
        """
        This magic method is redefined to show class and id of Author object.
        """
        return f"<Author (id={self.id}, name={self.name}, surname={self.surname})>"

    @staticmethod
    def get_by_id(author_id):
        """
        Get author by ID.
        """
        return Author.objects.filter(id=author_id).first()

    @staticmethod
    def delete_by_id(author_id):
        """
        Deletes an author by ID.
        """
        author = Author.get_by_id(author_id)
        if author:
            author.delete()
            return True
        return False

    @staticmethod
    def create(name, surname, patronymic=None):
        """
        Creates a new author.
        """
        author = Author(name=name, surname=surname, patronymic=patronymic)
        author.save()
        return author

    def to_dict(self):
        """
        Returns author data as a dictionary.
        """
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "patronymic": self.patronymic
        }

    def update(self, name=None, surname=None, patronymic=None):
        """
        Updates author in the database with the specified parameters.
        """
        if name is not None:
            self.name = name
        if surname is not None:
            self.surname = surname
        if patronymic is not None:
            self.patronymic = patronymic
        self.save()

    @staticmethod
    def get_all():
        """
        Returns a QuerySet of all authors.
        """
        return Author.objects.all()
