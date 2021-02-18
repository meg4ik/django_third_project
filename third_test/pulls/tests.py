from django.test import TestCase

# Create your tests here.

import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from .models import Questions


def create_questions(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Questions.objects.create(questions_text=question_text, pub_date=time)

class QuestionsIndexViewTests(TestCase):

    def test_no_questions(self):
        response = self.client.get(reverse('pulls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No pulls are available.")
        self.assertQuerysetEqual(response.context['latest_que'], [])

    def test_past_question(self):
        create_questions("Past question", -30)
        response = self.client.get(reverse('pulls:index'))
        self.assertQuerysetEqual(response.context['latest_que'], ['<Question: Past question>'])

    def test_future_question(self):
        create_questions("Future question", 30)
        response = self.client.get(reverse('pulls:index'))
        self.assertContains(response, "No pulls are available.")
        self.assertQuerysetEqual(response.context['latest_que'], [])

    def test_future_question_and_past_question(self):
        create_questions("Past question", -30)
        create_questions("Future question", 30)
        response = self.client.get(reverse('pulls:index'))
        self.assertQuerysetEqual(response.context['latest_que'], ['<Question: Past question>'])

    def test_two_past_questions(self):
        create_questions("Past question 1", -30)
        create_questions("Future question 2", -5)
        response = self.client.get(reverse('pulls:index'))
        self.assertQuerysetEqual(response.context['latest_que'], ['<Question: Past question 1>', '<Question: Past question 2>'])

class QuesionDetailViewTests(TestCase):
    def test_future_question(self):
        future_question = create_questions("Future question", 5)
        response = self.client.get(reverse('pulls:detail', args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_questions("Past question", -5)
        response = self.client.get(reverse('pulls:detail', args=(past_question.id,)))
        self.assertContains(response, past_question.questions_text)


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