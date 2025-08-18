from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserTestModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='1234', email='test@gmail.com')


    def test_str_mtd(self):
        self.assertEqual(str(self.user), "testuser")

    # test user creation
    def test_create_and_retrieve_user(self):
        user = User.objects.get(username='testuser')
        self.assertEqual(user.email, "test@gmail.com")