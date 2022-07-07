
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login, name="login"),
    path('login/', views.login, name="login1"),
    path('register/', views.register, name="register"),
    path('profile/', views.profile, name="profile"),
    path('createquestion/', views.createquestion, name="createquestion"),
    path('votes/', views.votes, name="votes"),
]
