

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from articles.models import Article



User = get_user_model()

# Test cases for article permissions without login
class ArticlePermissionTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="1234")
        self.article = Article.objects.create(
            title="Test Article",
            content="Test Content",
            author=self.user,
            status="approved"
        )

        self.articles_url = "/api/articles/"
        self.article_detail_url = f"/api/articles/{self.article.id}/"

    def test_post_article_without_login(self):
        
        response = self.client.post(self.articles_url, {
            "title": "New Article",
            "content": "New Content"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_article_without_login(self):
        
        response = self.client.put(self.article_detail_url, {
            "title": "Updated",
            "content": "Updated content"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_article_without_login(self):
        
        response = self.client.delete(self.article_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)




class ArticleApproveRejectTests(TestCase):

    def setUp(self):
        self.admin = User.objects.create_user(username="admin", password="1234", role="admin")
        self.member = User.objects.create_user(username="member", password="1234", role="member")
        self.normal = User.objects.create_user(username="normal", password="1234", role="normal")

        self.article = Article.objects.create(
            title="Pending Article",
            content="Test Content",
            author=self.member,
            status="pending"
        )

        self.approve_url = f"/api/articles/{self.article.id}/approve/"
        self.reject_url = f"/api/articles/{self.article.id}/reject/"

    def test_normal_user_cannot_approve(self):
        self.client.login(username="normal", password="1234")
        response = self.client.put(self.approve_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_member_user_cannot_approve(self):
        self.client.login(username="member", password="1234")
        response = self.client.put(self.approve_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_approve(self):
        self.client.login(username="admin", password="1234")
        response = self.client.put(self.approve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.article.refresh_from_db() # dobare grftn article az db bry motmaen bodan az change
        self.assertEqual(self.article.status, "approved")

    def test_admin_can_reject(self):
        self.client.login(username="admin", password="1234")
        response = self.client.put(self.reject_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.article.refresh_from_db()
        self.assertEqual(self.article.status, "rejected")
