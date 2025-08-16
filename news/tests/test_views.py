from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from news.models import News

User = get_user_model()

# test api views for news

class NewsViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.member = User.objects.create_user(username="member", password="1234", role="member")
        self.normal = User.objects.create_user(username="normal", password="1234")
        self.news = News.objects.create(title="Test News", content="content", author=self.member)

    def test_post_news_only_member_or_admin(self):
        self.client.login(username="normal", password="1234")
        response = self.client.post("/api/news/", {"title": "New", "content": "c"})
        self.assertEqual(response.status_code, 403)

        self.client.login(username="member", password="1234")
        response = self.client.post("/api/news/", {"title": "New", "content": "c"})
        self.assertEqual(response.status_code, 201)

    def test_get_news_list(self):
        response = self.client.get("/api/news/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_put_delete_only_author_or_admin(self):
        self.client.login(username="member", password="1234")
        response = self.client.put(f"/api/news/{self.news.id}/", {"title": "Edited", "content": "Edited"})
        self.assertEqual(response.status_code, 200)
        response = self.client.delete(f"/api/news/{self.news.id}/")
        self.assertEqual(response.status_code, 204)




# test permissions and functionality of article views

class NewsViewTests(TestCase):

    def setUp(self):
        self.normal_user = User.objects.create_user(username="normal", password="1234", role="normal")
        self.member_user = User.objects.create_user(username="member", password="1234", role="member")
        self.admin_user = User.objects.create_user(username="admin", password="1234", role="admin")

        self.news_url = "/api/news/"
        self.payload = {
            "title": "Test News",
            "content": "Some news content"
        }

    def test_post_news_normal_user_forbidden(self):
        self.client.login(username="normal", password="1234")
        response = self.client.post(self.news_url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(News.objects.count(), 0)

    def test_post_news_member_user_allowed(self):
        self.client.login(username="member", password="1234")
        response = self.client.post(self.news_url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(News.objects.count(), 1)
        self.assertEqual(News.objects.first().author.username, "member")

    def test_post_news_admin_user_allowed(self):
        self.client.login(username="admin", password="1234")
        response = self.client.post(self.news_url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(News.objects.count(), 1)
        self.assertEqual(News.objects.first().author.username, "admin")

    def test_post_news_unauthenticated_forbidden(self):
        response = self.client.post(self.news_url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
