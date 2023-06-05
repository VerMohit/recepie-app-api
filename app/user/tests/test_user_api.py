"""
Test for user API
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls. import reverse

from rest_framework.test import APIClient
from rest_framework import status

# Add API url we're going to test as constant
# get url from name of view - user = app, create = endpoint
CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    """Create and return new user
    Helper function for creating users for testing
    **params lets us add any parameters we want to function call"""
    return get_user_model().objects.create_user(**params)


# make public test - unauthenticated requests (i.e registering new user)
class PublicUserApiTests(TestCase):
    """Test public features of the user API"""

    # Create an API client that can used for testing
    def setUp(self):
        self.client = APIClient()


    def test_create_user_success(self):
        """Test creating a user is successful"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }

        # Post data to API to perform test
        # HTTP post Request made to CREATE_USER_URL and pass in payload to be posed to the url
        res = self.client.post(CREATE_USER_URL, payload)

        # Test to see endpoint returns HTTP 201 created response - success response code for creating object in DB using an API
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Retrieve object from DB with email address passed in as payload
        user = get_user_model().objects.get(email=payload['email'])
        # Verify user was created after the post command above
        self.assertTrue(user.check_password(payload['password']))
        # Verify password hash is not returned from API - security check
        self.assertNotIn('password', res.data)

    # Edge cases, where user is not created/added
    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }

        # Create use with details passed in from payload
        create_user(**payload)

        # Make post request
        res = self.client.post(CREATE_USER_URL, payload)

        # Test API returns HTTP 400 Bad Request response if new user registers with an existing email in DB
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQEUST)


    def test_password_too_short_error(self):
        """Test error is returned if password is < 5 chars"""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test Name',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQEUST)

        # Checks to see if the user already exists using filter and exists commands - boolean
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()

        # Confirm user DNE in DB
        self.assertFalse(user_exists)


# make private test -