from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.template import loader
from django.shortcuts import redirect, render
from waste_watcher.models import User, Trashbin
from django.views.decorators.csrf import csrf_exempt
from webpush import send_group_notification
from pathlib import Path
import random, string
import secrets
import base64
from datetime import datetime
import math

BASE_DIR = Path(__file__).resolve().parent.parent

global_pass = ""


def scoreboard(request: HttpRequest):
    if request.method == "GET":
        
        # password = request.GET.get("pass")
        #if not check_password(password):
        #    return HttpResponse("Authentication failed")
        
        try:
            users = list(User.objects.values())
            users.sort(key=lambda u: u['score'], reverse=True)
        except:
            users = []
        template = loader.get_template("scoreboard.html")
        trashbin = get_trashbin_model()
        first = None
        if len(users) > 1:
            first = users[0]
            users = users[1:]
        context = {"first": first, "users": users, "fillstate": int(trashbin.amount)}
        return HttpResponse(template.render(context, request))
    return HttpResponse("Wrong Method")


def commit(request: HttpRequest):
    if request.method == "GET":
        id = request.GET.get("id")
        user = User.objects.get(id=id)
        points = calculate_points(user)
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
        
        timestamp = datetime(2000, 1, 1)
        score = 0
        user: User = User(id=id, score=score, name=username, last_time_used=timestamp)
        if User.objects.all().filter(id=id).exists():
            return HttpResponse("User already exists")
        user.save()
        return HttpResponse("User created")
    return HttpResponse("Method not implemented")


def delete_user(request: HttpRequest):
    if request.method == "GET":
        id = request.GET.get("id")
        if not User.objects.all().filter(id=id).exists():
            return HttpResponse("User not found")
        User.objects.all().filter(id=id).delete()
        return HttpResponse("User deleted")
    return HttpResponse("Method not implemented")


def reset(request: HttpRequest):
    if request.method == "GET":
        try:
            User.objects.all().delete()
        except:
            return HttpResponse("Something went wrong when deleting all users")
        return HttpResponse("The database has been cleared")
    return HttpResponse("Wrong Method")


def sub(request: HttpRequest):
    webpush = {"group": "waste"}
    context = {"webpush": webpush}
    if request.method == "GET":        #send_group_notification(group_name="waste", payload="worked", ttl=1000)
        template = loader.get_template("subscribe.html")
        return HttpResponse(template.render(context, request))
    
    
def notify(request:HttpRequest):
    if request.method == "GET":
        payload = {"head": "Waste Watcher - Interactive Systems", "body": "Trash is full", "icon": "https://images.pexels.com/photos/3806764/pexels-photo-3806764.jpeg"}
        send_group_notification(group_name="waste", payload=payload, ttl=1000)
        return HttpResponse("Send test notifcation")
    return HttpResponse("Wrong Method")


def index(request: HttpRequest):
    response = redirect("/scoreboard")
    return response


def controls(request: HttpRequest):
    if request.method == "GET":
        template = loader.get_template("admin.html")
        security_check = randomword(5)
        context = {"sec_check": security_check}
        return HttpResponse(template.render(context, request))
    return HttpResponse("Wrong Method")


def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))


def calculate_points(user: User):
    last_time = datetime.timestamp(user.last_time_used)
    current_time = datetime.timestamp(datetime.now())
    time_diff = int(current_time-last_time)
    points = min(50, math.ceil(time_diff / 1728))
    return points


def set_fill_amount(request: HttpRequest):
    if request.method == "GET":
        try:
            amount = float(request.GET.get("amount"))
        except:
            return HttpResponse("Method not implemented")
        trashcan = get_trashbin_model()
        trashcan.amount = amount
        trashcan.save()
        
        return HttpResponse("Updated Trashcan amount")
    return HttpResponse("Method not implemented")


def set_max_amount(request: HttpRequest):
    if request.method == "GET":

        try:
            amount = float(request.GET.get("amount"))
        except:
            return HttpResponse("Method not implemented")
        trashcan = get_trashbin_model()
        trashcan.amount = amount
        trashcan.save()
        
        return HttpResponse("Updated max Trashcan amount")
    return HttpResponse("Method not implemented")


def get_trashbin_model():
    if Trashbin.objects.all().filter(id=0).exists():
        return Trashbin.objects.get(id=0)
    t = Trashbin(id=0)
    t.save()
    return t
