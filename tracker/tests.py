from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import expense


class PerUserDataTests(TestCase):
    def setUp(self):
        self.a = User.objects.create_user("alice", password="pass12345!x")
        self.b = User.objects.create_user("bob", password="pass12345!x")
        self.a_item = expense.objects.create(Expense_reason="Chai", Amount=10, user=self.a)
        self.b_item = expense.objects.create(Expense_reason="Pizza", Amount=500, user=self.b)

    def test_login_required(self):
        r = self.client.get(reverse("index"))
        self.assertEqual(r.status_code, 302)
        self.assertIn("/login/", r.url)

    def test_user_sees_only_own_expenses(self):
        self.client.login(username="alice", password="pass12345!x")
        r = self.client.get(reverse("index"))
        self.assertContains(r, "Chai")
        self.assertNotContains(r, "Pizza")

    def test_new_item_belongs_to_logged_in_user(self):
        self.client.login(username="alice", password="pass12345!x")
        self.client.post(reverse("add_item"), {"Expense_reason": "Bus", "Amount": 20, "Image": ""})
        item = expense.objects.get(Expense_reason="Bus")
        self.assertEqual(item.user, self.a)

    def test_cannot_open_edit_delete_others_item(self):
        self.client.login(username="alice", password="pass12345!x")
        for name in ("detail", "update_item", "delete_item"):
            r = self.client.get(reverse(name, args=[self.b_item.id]))
            self.assertEqual(r.status_code, 404, name)
        self.client.post(reverse("delete_item", args=[self.b_item.id]))
        self.assertTrue(expense.objects.filter(pk=self.b_item.id).exists())

    def test_total_only_counts_own_items(self):
        self.client.login(username="alice", password="pass12345!x")
        r = self.client.get(reverse("pdf"))
        self.assertEqual(r.context["total_sum"], 10)


class SignupLoginTests(TestCase):
    def test_signup_logs_user_in_and_goes_to_list(self):
        r = self.client.post(reverse("register"), {
            "username": "newuser", "password1": "Strong#Pass123", "password2": "Strong#Pass123",
        })
        self.assertRedirects(r, reverse("index"))
        self.assertIn("_auth_user_id", self.client.session)

    def test_bad_signup_shows_errors_on_same_page(self):
        r = self.client.post(reverse("register"), {
            "username": "x", "password1": "123", "password2": "123",
        })
        self.assertEqual(r.status_code, 200)  # stays on sign-up page
        self.assertTrue(r.context["form"].errors)

    def test_logged_in_user_skips_signup_and_login_pages(self):
        User.objects.create_user("carol", password="pass12345!x")
        self.client.login(username="carol", password="pass12345!x")
        self.assertRedirects(self.client.get(reverse("register")), reverse("index"))
        self.assertRedirects(self.client.get(reverse("login")), reverse("index"))
