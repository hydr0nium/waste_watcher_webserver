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

    @classmethod
    def setUpClass(cls):
        super(ServerTest, cls).setUpClass()
        with open("password.txt", "r") as f:
            cls.password = f.readline().strip()

    def test_scoreboard(self):
        c = Client()
        res = c.get(f"/scoreboard?pass={ServerTest.password}")
        res = res.content.decode("utf-8").replace("\n", "").replace(" ", "")
        self.assertIn("<body></body>", res)

    def test_useradd(self):
        c = Client()
        res = c.get(f"/add_user?id=4&username=Testuser&pass={ServerTest.password}")
        self.assertIn("User created", res.content.decode("utf-8"))

    def test_commit(self):
        c = Client()
        res = c.get(f"/add_user?id=4&username=Testuser&pass={ServerTest.password}")
        res = c.get(f"/commit?id=4&pass={ServerTest.password}")
        self.assertIn("Score of User", res.content.decode("utf-8"))

    def test_set_fill(self):
        c = Client()
        res = c.get(f"/set_fill_amount?amount=30&pass={ServerTest.password}")
        self.assertIn("Updated Trashcan amount", res.content.decode("utf-8"))

    def test_max_fill(self):
        c = Client()
        res = c.get(f"/set_max_amount?amount=30&pass={ServerTest.password}")
        self.assertIn("Updated max Trashcan amount", res.content.decode("utf-8"))

    def test_resetdb(self):
        c = Client()
        res = c.get(f"/add_user?id=4&username=Testuser&pass={ServerTest.password}")
        res = c.get(f"/commit?id=4&pass={ServerTest.password}")
        res = c.get(f"/reset?pass={ServerTest.password}")
        self.assertIn("The database has been cleared", res.content.decode())
        res = c.get(f"/scoreboard?pass={ServerTest.password}")
        res = res.content.decode("utf-8").replace("\n", "").replace(" ", "")
        self.assertIn("<body></body>", res)

    def test_user_already_in_db(self):
        c = Client()
        res = c.get(f"/add_user?id=4&username=Testuser&pass={ServerTest.password}")
        res = c.get(f"/add_user?id=4&username=Testuser2&pass={ServerTest.password}")
        self.assertIn("User already exists", res.content.decode("utf-8"))

        
