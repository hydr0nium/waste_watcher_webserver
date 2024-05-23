from django.http import HttpRequest, HttpResponse
from django.template import loader
from django.shortcuts import redirect 
from waste_watcher.models import User
from django.views.decorators.csrf import csrf_exempt
from webpush import send_group_notification

def scoreboard(request: HttpRequest):
    try:
        users = list(User.objects.values())
    except:
        users = []
    template = loader.get_template("scoreboard.html")
    context = {"users": users}
    return HttpResponse(template.render(context, request))

def commit(request: HttpRequest):
    if request.method == "GET":
        id = request.GET.get("id")
        points = request.GET.get("points")
        user = User.objects.get(id=id)
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
        score = 0
        user: User = User(id=id, score=score, name=username)
        if User.objects.all().filter(id=id).exists():
            return HttpResponse("User already exists")
        user.save()
        return HttpResponse("User created")
    return HttpResponse("Method not implemented")

def reset(request: HttpRequest):
    try:
        User.objects.all().delete()
    except:
        return HttpResponse("Something went wrong when deleting all users")
    return HttpResponse("The database has been cleared")


def sub(request: HttpRequest):
    webpush = {"group": "waste"}
    context = {"webpush": webpush}
    if request.method == "GET":
        #send_group_notification(group_name="waste", payload="worked", ttl=1000)
        template = loader.get_template("subscribe.html")
        return HttpResponse(template.render(context, request))

def index(request: HttpRequest):
    response = redirect("/scoreboard")
    return response

