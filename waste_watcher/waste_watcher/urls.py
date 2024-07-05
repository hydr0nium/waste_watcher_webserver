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
    path('', views.index, name="index"),
    path('api/controls', views.controls, name="controls"),
    path('scoreboard', views.scoreboard, name="scoreboard"),
    path('api/commit', views.commit, name="commit"),
    path('api/reset', views.reset, name="reset"),
    path('api/add_user', views.add_user, name="add_user"),
    path('sub', views.sub, name="sub"),
    path('api/notify', views.notify, name="test"),
    path("api/delete_user", views.delete_user, name="delete_user"),
    path("api/set_fill_amount", views.set_fill_amount, name="set_fill_amount"),
    path("api/set_max_amount", views.set_max_amount, name="set_max_amount"),
    path('webpush/', include('webpush.urls'))
]
