from django.test import TestCase
from django.contrib.auth import get_user_model
from news.models import News

User = get_user_model()

class NewsTestModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='1234')
        self.news = News.objects.create(
            title="Test News",
            content="Some news content",
            author=self.user
        )


    def test_str_method(self):
        self.assertEqual(str(self.news), "Test News")


    def test_news_author_relationship(self):
        self.assertEqual(self.news.author.username, "testuser")


    def test_delete_user_cascades_news(self):
        self.user.delete()
        self.assertEqual(News.objects.count(), 0)