from django.test import TestCase
from django.contrib.auth import get_user_model
from articles.models import Article
from comments.models import Comment

# test comment for Article , for news & event is same just FK is diffrent

User = get_user_model()

class CommentTestModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='1234')
        self.article = Article.objects.create(
            title="Test Article",
            content="Test Content",
            author=self.user,
            status="approved" # bry test mishe status dad ba inke readonly hast to seiralizr
        )
        self.comment = Comment.objects.create(
            author=self.user,
            article=self.article,
            content="This is a test comment"
        )

    # test str mtd
    def test_str_method(self):
        self.assertIn("This is a test comment", str(self.comment))

    # test comment's user and article 
    def test_comment_relationship(self):
        self.assertEqual(self.comment.author.username, "testuser")
        self.assertEqual(self.comment.article.title, "Test Article")

    # test if article del => comment del
    def test_delete_article_cascades_comments(self):
        self.article.delete()
        self.assertEqual(Comment.objects.count(), 0)

    # test if user del => comment del
    def test_delete_user_cascades_comments(self):
        self.user.delete()
        self.assertEqual(Comment.objects.count(), 0)