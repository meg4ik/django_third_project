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

    def tets_was_published_recently_with_old_quetions(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Questions(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def tets_was_published_recently_with_recent_quetions(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Questions(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), False)