from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from articles.models import Article

User = get_user_model()


# test api views for articles

class ArticleViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="user", password="1234")
        self.admin = User.objects.create_user(username="admin", password="1234", role="admin")
        self.article = Article.objects.create(
            title="Approved Article",
            content="Content",
            author=self.user,
            status="approved"
        )

    def test_get_approved_articles(self):
        response = self.client.get("/api/articles/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_post_article_logged_in(self):
        self.client.login(username="user", password="1234")
        response = self.client.post("/api/articles/", {"title": "New", "content": "New content"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Article.objects.count(), 2)

    def test_detail_view_access_control(self):

        response = self.client.get(f"/api/articles/{self.article.id}/")
        self.assertEqual(response.status_code, 200)

    def test_update_delete_only_by_author(self):
        self.client.login(username="user", password="1234")
        response = self.client.put(f"/api/articles/{self.article.id}/", {"title": "Updated", "content": "Edited"})
        self.assertEqual(response.status_code, 200)
        response = self.client.delete(f"/api/articles/{self.article.id}/")
        self.assertEqual(response.status_code, 204)

    def test_my_articles_view(self):
        self.client.login(username="user", password="1234")
        response = self.client.get("/api/articles/my/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)





# test permissions and functionality of article views

class ArticleViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="user1", password="1234")
        self.other_user = User.objects.create_user(username="user2", password="1234")

        
        self.article1 = Article.objects.create(
            title="Approved Article",
            content="Some content",
            status="approved",
            author=self.user
        )

       
        self.article2 = Article.objects.create(
            title="Pending Article",
            content="Some content",
            status="pending",
            author=self.other_user
        )

        self.list_url = "/api/articles/"
    
    def test_get_only_approved_articles(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [a["title"] for a in response.data]
        self.assertIn("Approved Article", titles) # check Approved Article in titles list
        self.assertNotIn("Pending Article", titles) # check Not Approved Article in titles list

    def test_post_article_logged_in_user(self):
        self.client.login(username="user1", password="1234")
        test_artic = {
            "title": "New Article",
            "content": "New Content"
        }
        response = self.client.post(self.list_url, test_artic)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Article")
        self.assertEqual(response.data["author"], "user1")
        self.assertEqual(response.data["status"], "pending")  
