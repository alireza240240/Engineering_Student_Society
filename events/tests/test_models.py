from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.timezone import now , timedelta

from events.models import Event , EventParticipant


User = get_user_model()

# test model create ...
class EventTestModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='1234')
        self.event = Event.objects.create(
            title = "TestEvent",
            description="Test Description",
            date = now() + timedelta(days=1),
            capacity = 10 ,
            creator = self.user
        )

    # test __str__ mtd
    def test_str_mtd(self):
        self.assertEqual(str(self.event),"TestEvent")

    # test spot_left() mtd
    def test_spot_left(self):
        # no register in first
        self.assertEqual(self.event.spots_left(),10)

        # after first register
        EventParticipant.objects.create(event=self.event , user=self.user)
        self.assertEqual(self.event.spots_left(),9)

    # test unique_participant in meta:unique_together
    def test_unique_participant(self):

        EventParticipant.objects.create(event=self.event , user=self.user)
        # ya type error ro bgo ya dr hlt koli Exception bnvs yni hr erri
        with self.assertRaises(Exception):
            EventParticipant.objects.create(event=self.event , user=self.user)
