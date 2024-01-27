from django.urls import path
from . import views

app_name='weatherapp'

urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.search, name="search"),
    path("signup/", views.signup, name="signup"),
    path("mycity/", views.mycity, name="mycity"),

    
    

    
]