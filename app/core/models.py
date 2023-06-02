"""
Database models for the proejct
"""
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)


# Create Custom manager for User Table
class UserManager(BaseUserManager):
    """Manager for the Custom User Model"""

    def create_user(self, email, password=None, **extra_field):
        """Create, save and return a new user"""

        # self.model() references the User table and this creates a new user model
        user = self.model(email=email, **extra_field)
        # Takes password and encrypts it using a hashing mechanism - security
        user.set_password(password)
        # saves user model. self._db supports adding mutliple DBs to proejct, BEST PRACTICE to pass this!
        user.save(using=self._db)

        return user


# Create custom user model
class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""

    # Attributes for the User table:
    # email is defined as unique
    email = models.EmailField(max_length=255, unique=True)
    # User enters their name
    name = models.CharField(max_length=255)
    # Users that register will by default be active in the system
    is_active = models.BooleanField(default=True)
    # Used to ensure only staff users can be logged in as admin
    is_staff = models.BooleanField(default=False)

    # Assign Manager to the custom uUser class
    objects = UserManager()

    # Field we want to use for authentication. Used to replace default username to custom field
    USERNAME_FIELD = 'email'
