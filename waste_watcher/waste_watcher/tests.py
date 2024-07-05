from django.test import TestCase
from django.test import Client
from .models import User

class UserModelTest(TestCase):

    user: User = User(id=1, score=30, name="Testuser")

    def test_name(self):
        self.assertEqual(self.user.name, "Testuser")
    
    def test_score(self):
        self.assertEqual(self.user.score, 30)

    def test_id(self):
        self.assertEqual(self.user.id, 1)


class ServerTest(TestCase):

    def test_scoreboard(self):
        c = Client()
        res = c.get(f"/scoreboard")
        res = res.content.decode("utf-8").replace("\n", "").replace(" ", "")
        self.assertIn("progress-bar", res)

    def test_useradd(self):
        c = Client()
        res = c.get(f"/add_user?id=4&username=Testuser")
        self.assertIn("User created", res.content.decode("utf-8"))

    def test_commit(self):
        c = Client()
        res = c.get(f"/add_user?id=4&username=Testuser")
        res = c.get(f"/commit?id=4")
        self.assertIn("Score of User", res.content.decode("utf-8"))

    def test_set_fill(self):
        c = Client()
        res = c.get(f"/set_fill_amount?amount=30")
        self.assertIn("Updated Trashcan amount", res.content.decode("utf-8"))

    def test_max_fill(self):
        c = Client()
        res = c.get(f"/set_max_amount?amount=30")
        self.assertIn("Updated max Trashcan amount", res.content.decode("utf-8"))

    def test_resetdb(self):
        c = Client()
        res = c.get(f"/add_user?id=4&username=Testuser")
        res = c.get(f"/commit?id=4")
        res = c.get(f"/reset")
        self.assertIn("The database has been cleared", res.content.decode())
        res = c.get(f"/scoreboard")
        res = res.content.decode("utf-8").replace("\n", "").replace(" ", "")
        self.assertNotIn("Testuser", res)

    def test_user_already_in_db(self):
        c = Client()
        res = c.get(f"/add_user?id=4&username=Testuser")
        res = c.get(f"/add_user?id=4&username=Testuser2")
        self.assertIn("User already exists", res.content.decode("utf-8"))

        
