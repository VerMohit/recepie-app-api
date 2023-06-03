"""
Test for the Django admin modifications
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

class AdminSiteTests(TestCase):
    """Tests for django admin"""

    # Create setup method to set up modules at start of different tests in this class
    # This will be run before every single test
    def setUp(self):
        """Create user and client"""

        # Instance of CLient class, which is a test client to get http requests
        self.client = Client()
        # Create superuser
        self.admin_user = get_user_model().objects.create_superuser(email='admin@example.com', password='testpass123')
        # Force authentication of admin_user using client
        self.client.force_login(self.admin_user)

        # Create general user in DB
        self.user = get_user_model().objects.create_user(email='user@example.com', password='testpass123', name='Test User')

    def test_users_list(self):
        """Test that users are listed on page"""

        # reverse = get url for changed list inside django admin
        # admin:core_user_changelist = which url to pull from django admin - defined in django doc
        url = reverse('admin:core_user_changelist')

        # Make a get http request based to the url, which will be authenticated as admin_user
        res = self.client.get(url)

        # Check page contains user created and associated email
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test edit user page works"""

        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        # Ensure page loads successfully
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test the create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        # Ensure page loads successfully
        self.assertEqual(res.status_code, 200)
