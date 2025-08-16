from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from events.models import Event
from django.utils.timezone import now, timedelta

User = get_user_model()


# test api views for events

class EventViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.member = User.objects.create_user(username="member", password="1234", role="member")
        self.normal = User.objects.create_user(username="normal", password="1234")
        self.event = Event.objects.create(
            title="Test Event",
            description="desc",
            date=now() + timedelta(days=1),
            capacity=2,
            creator=self.member
        )

    def test_post_event_only_member_or_admin(self):
        self.client.login(username="normal", password="1234")
        response = self.client.post("/api/events/", {"title": "E", "description": "d", "date": now(), "capacity": 10})
        self.assertEqual(response.status_code, 403)

        self.client.login(username="member", password="1234")
        response = self.client.post("/api/events/", {"title": "E", "description": "d", "date": now(), "capacity": 10})
        self.assertEqual(response.status_code, 201)

    def test_get_event_list(self):
        response = self.client.get("/api/events/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_register_event_success(self):
        self.client.login(username="normal", password="1234")
        response = self.client.post(f"/api/events/{self.event.id}/register/")
        self.assertEqual(response.status_code, 201)





# test permissions and functionality of event views

class EventViewTests(TestCase):

    def setUp(self):
        self.normal_user = User.objects.create_user(username="normal", password="1234", role="normal")
        self.member_user = User.objects.create_user(username="member", password="1234", role="member")
        self.admin_user = User.objects.create_user(username="admin", password="1234", role="admin")

        self.events_url = "/api/events/"
        self.payload = {
            "title": "Test Event",
            "description": "Some event description",
            "date": (now() + timedelta(days=5)).isoformat(),
            "capacity": 50
        }

    def test_post_event_normal_user_forbidden(self):
        self.client.login(username="normal", password="1234")
        response = self.client.post(self.events_url, self.payload, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Event.objects.count(), 0)

    def test_post_event_member_user_allowed(self):
        self.client.login(username="member", password="1234")
        response = self.client.post(self.events_url, self.payload, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(Event.objects.first().creator.username, "member")

    def test_post_event_admin_user_allowed(self):
        self.client.login(username="admin", password="1234")
        response = self.client.post(self.events_url, self.payload, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(Event.objects.first().creator.username, "admin")

    def test_post_event_unauthenticated_forbidden(self):
        response = self.client.post(self.events_url, self.payload, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
