from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.template import loader
from django.shortcuts import redirect, render
from waste_watcher.models import User
from django.views.decorators.csrf import csrf_exempt
from webpush import send_group_notification
from pathlib import Path
import random, string
import secrets
import base64

BASE_DIR = Path(__file__).resolve().parent.parent

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
    return HttpResponse("Wrong Method")

def commit(request: HttpRequest):
    if request.method == "GET":
        id = request.GET.get("id")
        points = request.GET.get("points")
        user = User.objects.get(id=id)
        password = request.GET.get("pass")
        if not check_password(password) and not authorized(request):
            res = HttpResponse('Unauthorized', status=401)
            res["WWW-Authenticate"] = 'Basic realm="This is an easteregg. Good job", charset="UTF-8"'
            return res

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

        password = request.GET.get("pass")
        if not check_password(password) and not authorized(request):
            res = HttpResponse('Unauthorized', status=401)
            res["WWW-Authenticate"] = 'Basic realm="This is an easteregg. Good job", charset="UTF-8"'
            return res

        id = request.GET.get("id")
        username = request.GET.get("username")
            
        score = 0
        user: User = User(id=id, score=score, name=username)
        if User.objects.all().filter(id=id).exists():
            return HttpResponse("User already exists")
        user.save()
        return HttpResponse("User created")
    return HttpResponse("Method not implemented")

def delete_user(request: HttpRequest):
    if request.method == "GET":
        id = request.GET.get("id")
        password = request.GET.get("pass")
        if not check_password(password) and not authorized(request):
            res = HttpResponse('Unauthorized', status=401)
            res["WWW-Authenticate"] = 'Basic realm="This is an easteregg. Good job", charset="UTF-8"'
            return res
        if not User.objects.all().filter(id=id).exists():
            return HttpResponse("User not found")
        User.objects.all().filter(id=id).delete()
        return HttpResponse("User deleted")
    return HttpResponse("Method not implemented")

def reset(request: HttpRequest):
    if request.method == "GET": 
        password = request.GET.get("pass")
        if not check_password(password) and not authorized(request):
            res = HttpResponse('Unauthorized', status=401)
            res["WWW-Authenticate"] = 'Basic realm="This is an easteregg. Good job", charset="UTF-8"'
            return res
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
        if not check_password(password) and not authorized(request):
            res = HttpResponse('Unauthorized', status=401)
            res["WWW-Authenticate"] = 'Basic realm="This is an easteregg. Good job", charset="UTF-8"'
            return res
        #send_group_notification(group_name="waste", payload="worked", ttl=1000)
        template = loader.get_template("subscribe.html")
        return HttpResponse(template.render(context, request))
    
def test(request:HttpRequest):
    if request.method == "GET":
        password = request.GET.get("pass")
        if not check_password(password) and not authorized(request):
            res = HttpResponse('Unauthorized', status=401)
            res["WWW-Authenticate"] = 'Basic realm="This is an easteregg. Good job", charset="UTF-8"'
            return res
        payload = {"head": "Waste Watcher - Interactive Systems", "body": "Trash is full", "icon": "https://images.pexels.com/photos/3806764/pexels-photo-3806764.jpeg"}
        send_group_notification(group_name="waste", payload=payload, ttl=1000)
        return HttpResponse("Send test notifcation")
    return HttpResponse("Wrong Method")

def index(request: HttpRequest):
    response = redirect("/scoreboard")
    return response

def controls(request: HttpRequest):
    if request.method == "GET":
        password = request.GET.get("pass")
        if not check_password(password) and not authorized(request):
            res = HttpResponse('Unauthorized', status=401)
            res["WWW-Authenticate"] = 'Basic realm="This is an easteregg. Good job", charset="UTF-8"'
            return res
        template = loader.get_template("admin.html")
        password = load_password()
        security_check = randomword(5)
        context = {"pass": password, "sec_check": security_check}
        return HttpResponse(template.render(context, request))
    return HttpResponse("Wrong Method")



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
    return global_pass
            

def check_password(userpass: str):
    load_password()
    global global_pass
    if global_pass == userpass:
        return True
    return False

def authorized(request: HttpRequest):
    auth_header: str = request.META.get("HTTP_AUTHORIZATION")
    if auth_header is None:
        print("Not auth header")
        return False
    if "Basic" not in auth_header:
        print("Not basic auth header")
        return False
    print(auth_header)
    login_data = base64.b64decode(auth_header.split(" ")[1]).decode("utf-8")
    print(login_data)
    if ":" not in login_data:
        return False
    username = login_data.split(":")[0]
    password = login_data.split(":")[1]
    if username != "waste_watcher" and password != load_password():
        return False
    return True
    



def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

