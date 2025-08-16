
from django.test import TestCase
from django.contrib.auth import get_user_model
from articles.models import Article
from comments.models import Comment

User = get_user_model()

class CascadeDeleteUserTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="1234")
        self.article = Article.objects.create(
            title="Cascade Test Article",
            content="Some content",
            author=self.user,
            status="approved"
        )
        self.comment = Comment.objects.create(
            content="Test comment",
            author=self.user,
            article=self.article
        )

    def test_delete_user_deletes_articles_and_comments(self):
        self.user.delete()
        self.assertEqual(Article.objects.count(), 0, "User delete should remove related articles")
        self.assertEqual(Comment.objects.count(), 0, "User delete should remove related comments")
