"""
URL configuration for waste_watcher project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('controls', views.controls, name="controls"),
    path('', views.index, name="index"),
    path('scoreboard', views.scoreboard, name="scoreboard"),
    path('commit', views.commit, name="commit"),
    path('reset', views.reset, name="reset"),
    path('add_user', views.add_user, name="add_user"),
    path('sub', views.sub, name="sub"),
    path('test', views.test, name="test"),
    path("delete_user", views.delete_user, name="delete_user"),
    path('webpush/', include('webpush.urls'))
]
