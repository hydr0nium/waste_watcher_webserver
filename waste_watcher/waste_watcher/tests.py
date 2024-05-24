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
        res = c.get("/scoreboard?pass=testpass")
        res = res.content.decode("utf-8").replace("\n", "").replace(" ", "")
        self.assertIn("<body></body>", res)

    def test_useradd(self):
        c = Client()
        res = c.get("/add_user?id=4&username=Testuser&pass=testpass")
        self.assertIn("User created", res.content.decode("utf-8"))

    def test_commit(self):
        c = Client()
        res = c.get("/add_user?id=4&username=Testuser&pass=testpass")
        res = c.get("/commit?id=4&points=50&pass=testpass")
        self.assertIn("Score of User", res.content.decode("utf-8"))

    def test_resetdb(self):
        c = Client()
        res = c.get("/add_user?id=4&username=Testuser&pass=testpass")
        res = c.get("/commit?id=4&points=50&pass=testpass")
        res = c.get("/reset&pass=testpass")
        self.assertIn("The database has been cleared", res.content.decode())
        res = c.get("/scoreboard&pass=testpass")
        res = res.content.decode("utf-8").replace("\n", "").replace(" ", "")
        self.assertIn("<body></body>", res)

    def test_user_already_in_db(self):
        c = Client()
        res = c.get("/add_user?id=4&username=Testuser&pass=testpass")
        res = c.get("/add_user?id=4&username=Testuser2&pass=testpass")
        self.assertIn("User already exists", res.content.decode("utf-8"))

        
