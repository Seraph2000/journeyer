from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('dashboard.html', views.dashboard, name="dashboard"),
    path('about.html', views.about, name="about"),
]