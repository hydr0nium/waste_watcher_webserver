from django.http import HttpRequest, HttpResponse
from django.template import loader
from django.shortcuts import redirect 
from waste_watcher.models import User

def scoreboard(request: HttpRequest):
    try:
        users = list(User.objects.values())
    except:
        users = []
    template = loader.get_template("scoreboard.html")
    context = {"users": users}
    print(context)
    return HttpResponse(template.render(context, request))

def commit(request: HttpRequest):
    if request.GET:
        id = request.GET.get("id")
        points = request.GET.get("points")
        user = User.objects.get(id=id)
        try:
            user.score = user.score + int(points)
        except ValueError:
            return HttpResponse("Could not convert points to number")
        user.save()
        return HttpResponse(f"Score of User {user.id} updated to {user.score}")
    return HttpResponse("Method not implemented")

def add_user(request: HttpRequest):
    if request.GET:
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


def index(request: HttpRequest):
    response = redirect("/scoreboard")
    return response

