"""
Tests for models
"""
# Import base class for teests
from django.test import TestCase

# Let's us get default user model for project
# Best practice to use get_user_model because if we use custom user models then it
#  will be retrieved as the default model for that project
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating a user with email is successful"""

        # Test variables
        email = 'test@example.com'  # @example.com domain name is reserved name and used specifically for testing
        password = 'testpass123'

        # get_user_model() = call user model we defined
        # object = reference to custom manager we create
        # create_user() = invoke method from manager
        user = get_user_model().objects.create_user(email=email, password=password)

        # Assertion tests
        self.assertEqual(user.email, email)
        # checking hash password, provided by the BaseUserManager class in our model module
        self.assertTrue(user.check_password(password))
