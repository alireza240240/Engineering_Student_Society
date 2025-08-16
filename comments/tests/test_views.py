from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from articles.models import Article
from comments.models import Comment

User = get_user_model()

# test api views for comments

class CommentViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="user", password="1234")
        self.article = Article.objects.create(title="Art", content="c", author=self.user, status="approved")

    def test_post_comment_logged_in(self):
        self.client.login(username="user", password="1234")
        response = self.client.post(f"/api/comments/articles/{self.article.id}/", {"content": "hello"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.count(), 1)

    def test_get_comments_list(self):
        Comment.objects.create(content="hi", author=self.user, article=self.article)
        response = self.client.get(f"/api/comments/articles/{self.article.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)






# test permissions and functionality of comment views

class CommentViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="user1", password="1234")
        self.article = Article.objects.create(
            title="Test Article",
            content="Some content",
            author=self.user,
            status="approved"
        )

        self.url = f"/api/comments/articles/{self.article.id}/"


    # test unauthenticated user trying to post a comment
    def test_post_comment_unauthenticated_forbidden(self):
        response = self.client.post(self.url, {"content": "Hello world!"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Comment.objects.count(), 0)


    def test_post_comment_authenticated_success(self):
        self.client.login(username="user1", password="1234")
        response = self.client.post(self.url, {"content": "This is my comment"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # check if the comment was created
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.content, "This is my comment")
        self.assertEqual(comment.author.username, "user1")
        self.assertEqual(comment.article, self.article)


    def test_get_comments_list(self):
        # Get comments for an article
        Comment.objects.create(content="First comment", author=self.user, article=self.article)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["content"], "First comment")
