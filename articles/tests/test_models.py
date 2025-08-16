
from django.test import TestCase
from django.contrib.auth import get_user_model
from articles.models import Article

User = get_user_model()

class ArticleTestModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='1234')
        self.article = Article.objects.create(
            title="Test Article",
            content="This is a test content for article",
            author=self.user
        )


    def test_str_method(self):
        self.assertEqual(str(self.article), "Test Article")

    # check author is correct
    def test_article_author_relationship(self):
        self.assertEqual(self.article.author.username, "testuser")

   
    def test_delete_user_cascades_articles(self):
        self.user.delete()
        self.assertEqual(Article.objects.count(), 0)