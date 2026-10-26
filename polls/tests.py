from datetime import timedelta

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import Choice, Question


@override_settings(ALLOWED_HOSTS=["testserver"])
class PollsViewTests(TestCase):
    def setUp(self):
        self.question = Question.objects.create(
            question_text="What is your favorite color?",
            pub_date=timezone.now(),
        )
        self.choice = Choice.objects.create(
            question=self.question,
            choice_text="Blue",
        )

    def test_index_shows_five_latest_questions(self):
        questions = [
            Question.objects.create(
                question_text=f"Question {number}",
                pub_date=timezone.now() + timedelta(seconds=number),
            )
            for number in range(6)
        ]

        response = self.client.get(reverse("polls:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h1>Polls</h1>", html=True)
        self.assertEqual(len(response.context["latest_question_list"]), 5)
        self.assertEqual(
            list(response.context["latest_question_list"]),
            list(reversed(questions[1:])),
        )

    def test_detail_shows_question_and_choices(self):
        response = self.client.get(reverse("polls:detail", args=(self.question.pk,)))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.question.question_text)
        self.assertContains(response, self.choice.choice_text)

    def test_detail_returns_404_for_unknown_question(self):
        response = self.client.get(reverse("polls:detail", args=(999,)))

        self.assertEqual(response.status_code, 404)

    def test_vote_without_choice_renders_error(self):
        response = self.client.post(reverse("polls:vote", args=(self.question.pk,)))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["error_message"], "You didn't select a choice."
        )
        self.assertEqual(self.choice.votes, 0)

    def test_vote_increments_choice_and_redirects_to_results(self):
        response = self.client.post(
            reverse("polls:vote", args=(self.question.pk,)),
            {"choice": self.choice.pk},
        )

        self.assertRedirects(
            response,
            reverse("polls:results", args=(self.question.pk,)),
        )
        self.choice.refresh_from_db()
        self.assertEqual(self.choice.votes, 1)

    def test_results_show_vote_count(self):
        self.choice.votes = 2
        self.choice.save()

        response = self.client.get(reverse("polls:results", args=(self.question.pk,)))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Blue -- 2 votes")
