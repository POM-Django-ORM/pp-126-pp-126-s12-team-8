from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _

ROLE_CHOICES = (
    (0, 'visitor'),
    (1, 'admin'),
)


class CustomUser(AbstractBaseUser):
    """
        This class represents a basic user.
    """

    first_name = models.CharField(max_length=20, blank=True, null=True)
    middle_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True, max_length=100)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.IntegerField(choices=ROLE_CHOICES, default=0)  # 0 - visitor, 1 - admin
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        """
        Magic method is redefined to show all information about CustomUser.
        """
        return f"{self.id}: {self.first_name} {self.middle_name or ''} {self.last_name} - {self.email}"

    def __repr__(self):
        """
        This magic method is redefined to show class and id of CustomUser object.
        """
        return f"<CustomUser (id={self.id}, email={self.email})>"

    @staticmethod
    def get_by_id(user_id):
        """
        Get user by ID.
        """
        return CustomUser.objects.filter(id=user_id).first()

    @staticmethod
    def get_by_email(email):
        """
        Returns user by email.
        """
        return CustomUser.objects.filter(email=email).first()

    @staticmethod
    def delete_by_id(user_id):
        """
        Deletes a user by ID.
        """
        user = CustomUser.get_by_id(user_id)
        if user:
            user.delete()
            return True
        return False

    @staticmethod
    def create(email, password, first_name=None, middle_name=None, last_name=None):
        """
        Creates a new user.
        """
        user = CustomUser(email=email, first_name=first_name, middle_name=middle_name, last_name=last_name)
        user.set_password(password)
        user.save()
        return user

    def to_dict(self):
        """
        Returns user data as a dictionary.
        """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "email": self.email,
            "created_at": int(self.created_at.timestamp()),
            "updated_at": int(self.updated_at.timestamp()),
            "role": self.role,
            "is_active": self.is_active
        }

    def update(self, first_name=None, last_name=None, middle_name=None, password=None, role=None, is_active=None):
        """
        Updates user profile in the database with the specified parameters.
        """
        if first_name is not None:
            self.first_name = first_name
        if middle_name is not None:
            self.middle_name = middle_name
        if last_name is not None:
            self.last_name = last_name
        if password is not None:
            self.set_password(password)
        if role is not None:
            self.role = role
        if is_active is not None:
            self.is_active = is_active
        self.save()

    @staticmethod
    def get_all():
        """
        Returns a QuerySet of all users.
        """
        return CustomUser.objects.all()

    def get_role_name(self):
        """
        Returns the role name as a string.
        """
        return dict(ROLE_CHOICES).get(self.role, "Unknown")
