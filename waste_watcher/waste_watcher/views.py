from django.http import HttpRequest, HttpResponse
from django.template import loader
from django.shortcuts import redirect 
from waste_watcher.models import User
from django.views.decorators.csrf import csrf_exempt
from webpush import send_group_notification
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
import secrets

global_pass = ""

def scoreboard(request: HttpRequest):
    if request.method == "GET":
        
        # password = request.GET.get("pass")
        #if not check_password(password):
        #    return HttpResponse("Authentication failed")
        
        try:
            users = list(User.objects.values())
        except:
            users = []
        template = loader.get_template("scoreboard.html")
        context = {"users": users}
        return HttpResponse(template.render(context, request))
    return HttpResonse("Wrong Method")

def commit(request: HttpRequest):
    if request.method == "GET":
        id = request.GET.get("id")
        points = request.GET.get("points")
        user = User.objects.get(id=id)
        password = request.GET.get("pass")
        if not check_password(password):
            return HttpResponse("Authentication failed")
        try:
            points = int(points)
            user.score = user.score + points
        except ValueError:
            return HttpResponse("Could not convert points to number")
        user.save()
        if points >= 500:
            payload = {"head": "Waste Watcher - Interactive Systems", "body": "Trash is full", "icon": "https://images.pexels.com/photos/3806764/pexels-photo-3806764.jpeg"}

            send_group_notification(group_name="waste", payload=payload, ttl=1000)
        return HttpResponse(f"Score of User {user.id} updated to {user.score}")
    return HttpResponse("Method not implemented")

def add_user(request: HttpRequest):
    if request.method == "GET":
        id = request.GET.get("id")
        username = request.GET.get("username")
        password = request.GET.get("pass")
        if not check_password(password):
            return HttpResponse("Authentication failed")
        score = 0
        user: User = User(id=id, score=score, name=username)
        if User.objects.all().filter(id=id).exists():
            return HttpResponse("User already exists")
        user.save()
        return HttpResponse("User created")
    return HttpResponse("Method not implemented")

def reset(request: HttpRequest):
    if request.method == "GET": 
        password = request.GET.get("pass")
        if not check_password(password):
            return HttpResponse("Authentication failed")
        try:
            User.objects.all().delete()
        except:
            return HttpResponse("Something went wrong when deleting all users")
        return HttpResponse("The database has been cleared")
    return HttpResponse("Wrong Method")

def sub(request: HttpRequest):
    webpush = {"group": "waste"}
    context = {"webpush": webpush}
    if request.method == "GET":
        password = request.GET.get("pass")
        if not check_password(password):
            return HttpResponse("Authentication failed")
        #send_group_notification(group_name="waste", payload="worked", ttl=1000)
        template = loader.get_template("subscribe.html")
        return HttpResponse(template.render(context, request))
    
def test(request:HttpRequest):
    if request.method == "GET":
        password = request.GET.get("pass")
        if not check_password(password):
            return HttpResponse("Authentication failed")
        payload = {"head": "Waste Watcher - Interactive Systems", "body": "Trash is full", "icon": "https://images.pexels.com/photos/3806764/pexels-photo-3806764.jpeg"}
        send_group_notification(group_name="waste", payload=payload, ttl=1000)
        return HttpResponse("Send test notifcation")
    return HttpResponse("Wrong Method")

def index(request: HttpRequest):
    response = redirect("/scoreboard")
    return response


def load_password():
    global global_pass
    if global_pass == "":
        try:
            with open(BASE_DIR / 'password.txt', 'r') as f:
                global_pass = f.read().strip()
        except FileNotFoundError:
            global_pass = secrets.token_urlsafe(42)
            with open(BASE_DIR / 'password.txt', 'w') as f:
                f.write(global_pass)
            

def check_password(userpass: str):
    load_password()
    global global_pass
    if global_pass == userpass:
        return True
    return False

