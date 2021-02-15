from django.test import TestCase

# Create your tests here.

import datetime

from django.utils import timezone
from django.test import TestCase

from .models import Questions

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_que = Questions(pub_date=time)
        self.assertIs(future_que.was_published_recently(), False)
