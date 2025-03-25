from django.db import models
from django.utils import timezone
from authentication.models import CustomUser

class Order(models.Model):
    book = models.ForeignKey('book.Book', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, default=timezone.now)
    end_at = models.DateTimeField(null=True, blank=True)
    plated_end_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """
        Magic method is redefined to show all information about Order.
        :return: order id, book name, user id, order created_at, order end_at, order plated_end_at
        """
        return f"Order {self.id}: Book '{self.book.name}' by {self.user.first_name} {self.user.last_name} - Created: {self.created_at}, Plated Return: {self.plated_end_at}, Returned: {self.end_at}"

    def __repr__(self):
        """
        This magic method is redefined to show class and id of Order object.
        :return: class, id
        """
        return f'{self.__class__.__name__}(id={self.id})'

    def to_dict(self):
        """
        :return: dict contains order id, book id, user id, order created_at, order end_at, order plated_end_at
        :Example:
        | {
        |   'id': 8,
        |   'book': 8,
        |   'user': 8,
        |   'created_at': 1509393504,
        |   'end_at': 1509393504,
        |   'plated_end_at': 1509402866,
        | }
        """
        return {
            'id': self.id,
            'book': self.book.id,
            'user': self.user.id,
            'created_at': int(self.created_at.timestamp()) if self.created_at else None,
            'end_at': int(self.end_at.timestamp()) if self.end_at else None,
            'plated_end_at': int(self.plated_end_at.timestamp()) if self.plated_end_at else None
        }

    @staticmethod
    def create(user, book, plated_end_at):
        """
        :param user: the user who took the book
        :type user: CustomUser
        :param book: the book they took
        :type book: Book
        :param plated_end_at: planned return of data
        :type plated_end_at: int (timestamp)
        :return: a new order object which is also written into the DB
        """
        order = Order(user=user, book=book, plated_end_at=plated_end_at)
        order.save()
        return order

    @staticmethod
    def get_by_id(order_id):
        """
        :param order_id: the id of the order
        :type order_id: int
        :return: the object of the order, according to the specified id or None in case of its absence
        """
        return Order.objects.filter(id=order_id).first()

    def update(self, plated_end_at=None, end_at=None):
        """
        Updates order in the database with the specified parameters.
        :param plated_end_at: new plated_end_at
        :type plated_end_at: int (timestamp)
        :param end_at: new end_at
        :type end_at: int (timestamp)
        :return: None
        """
        if plated_end_at:
            self.plated_end_at = plated_end_at
        if end_at:
            self.end_at = end_at
        self.save()

    @staticmethod
    def get_all():
        """
        :return: all orders
        """
        return Order.objects.all()

    @staticmethod
    def get_not_returned_books():
        """
        :return: all orders that do not have a return date (end_at)
        """
        return Order.objects.filter(end_at__isnull=True)

    @staticmethod
    def delete_by_id(order_id):
        """
        :param order_id: an id of a user to be deleted
        :type order_id: int
        :return: True if object existed in the db and was removed or False if it didn't exist
        """
        order = Order.get_by_id(order_id)
        if order:
            order.delete()
            return True
        return False
