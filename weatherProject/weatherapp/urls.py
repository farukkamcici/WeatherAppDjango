from django.urls import path
from . import views

app_name='weatherapp'

urlpatterns = [
    path("", views.grid, name="grid"),
    path("search/", views.search, name="search"),
    path("signup/", views.signup, name="signup"),
    
    

    
]