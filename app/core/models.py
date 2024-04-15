"""
Database models.
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users."""

    # @classmethod
    def normalize_email(self, email):
        """
        Normalize the email address by lowercasing the domain part of it.
        """
        email = email or ""
        try:
            email_name, domain_part = email.strip().rsplit("@", 1)
        except ValueError:
            pass
        else:
            email = email_name.lower() + "@" + domain_part.lower()
        return email

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return new user."""
        if not email:
            raise ValueError("User must have an email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class FriendRequest(models.Model):
    """Friend Request in the system."""

    sender = models.ForeignKey(
        User, related_name="sender", on_delete=models.CASCADE, null=True
    )
    receiver = models.ForeignKey(
        User, related_name="receiver", on_delete=models.CASCADE, null=True
    )
    status = models.CharField(max_length=20, default="pending")

    def __str__(self):
        return f"{self.sender.name} to {self.receiver.name}"


class Friend(models.Model):
    """Friend relationship between two users."""

    user1 = models.ForeignKey(
        User, related_name="friend_1", on_delete=models.CASCADE, null=True
    )
    user2 = models.ForeignKey(
        User, related_name="friend_2", on_delete=models.CASCADE, null=True
    )

    def __str__(self):
        return f"{self.user1.name} is friends with {self.user2.name}"
