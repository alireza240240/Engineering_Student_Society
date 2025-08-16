from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from events.models import Event, EventParticipant
from django.utils.timezone import now, timedelta

User = get_user_model()

class EventRegistrationTests(TestCase):

    def setUp(self):
        self.member = User.objects.create_user(username="member", password="1234", role="member")
        self.other_user = User.objects.create_user(username="other", password="1234", role="member")

        self.event = Event.objects.create(
            title="Test Event",
            description="Some description",
            date=now() + timedelta(days=1),
            capacity=1,
            creator=self.member
        )

        self.url = f"/api/events/{self.event.id}/register/"

    def test_cannot_register_if_event_is_full(self):
        
        # first registration by the member
        EventParticipant.objects.create(event=self.event, user=self.member)

        # second registration by another user
        self.client.login(username="other", password="1234")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("capacity", response.data.get("error", "").lower())

    def test_cannot_register_twice_for_same_event(self):
        # test registration by the member
        EventParticipant.objects.create(event=self.event, user=self.member)

        # attempt to register again
        self.client.login(username="member", password="1234")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already", response.data.get("error", "").lower())
