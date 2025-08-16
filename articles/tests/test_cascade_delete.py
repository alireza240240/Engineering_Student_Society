
from django.test import TestCase
from django.contrib.auth import get_user_model
from articles.models import Article
from comments.models import Comment

User = get_user_model()

class CascadeDeleteArticleTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="1234")
        self.article = Article.objects.create(
            title="Cascade Delete Article",
            content="Cascade test content",
            author=self.user,
            status="approved"
        )
        self.comment = Comment.objects.create(
            content="Related comment",
            author=self.user,
            article=self.article
        )

    def test_delete_article_deletes_comments(self):
        self.article.delete()
        self.assertEqual(Comment.objects.count(), 0, "Deleting article should also delete related comments")
