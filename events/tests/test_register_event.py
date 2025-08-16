from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from events.models import Event, EventParticipant
from django.utils.timezone import now, timedelta

User = get_user_model()

class RegisterEventTests(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="1234", role="member")
        self.user2 = User.objects.create_user(username="user2", password="1234", role="normal")
        self.user3 = User.objects.create_user(username="user3", password="1234", role="normal")

        self.event = Event.objects.create(
            title="Test Event",
            description="Some event description",
            date=now() + timedelta(days=2),
            capacity=2,
            creator=self.user1
        )

        self.register_url = f"/api/events/{self.event.id}/register/"

    def test_register_event_unauthenticated_forbidden(self):
        response = self.client.post(self.register_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(EventParticipant.objects.count(), 0)

    def test_register_event_success(self):
        self.client.login(username="user1", password="1234")
        response = self.client.post(self.register_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EventParticipant.objects.count(), 1)
        self.assertEqual(EventParticipant.objects.first().user.username, "user1")

    def test_register_event_full_capacity(self):
        

        EventParticipant.objects.create(event=self.event, user=self.user1)
        EventParticipant.objects.create(event=self.event, user=self.user2)

        self.client.login(username="user3", password="1234")
        response = self.client.post(self.register_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Capacity", response.json()["error"])

    def test_register_event_duplicate_registration(self):
        self.client.login(username="user1", password="1234")
        EventParticipant.objects.create(event=self.event, user=self.user1)

        response = self.client.post(self.register_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Alredy Registered", response.json()["error"])
