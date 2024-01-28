from collections.abc import Callable, Iterable, Mapping
from typing import Any
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
import requests
import pytz
from datetime import datetime,timedelta
from django.contrib.auth import login, authenticate 
from .forms import SignUpForm
from threading import Thread
from .utils import timezone_conv

        
def get_city_info(city):
    api_key = "7ed79061f55449a1a76205741242401"
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    response = requests.get(url).json()  
    
    name = response["location"]["name"]
    country= response["location"]["country"]
    curr_temp_c = round(response["current"]["temp_c"])
    curr_cond_icon = response["current"]["condition"]["icon"]
    curr_cond_desc = response["current"]["condition"]["text"]
    last_upd_loc = response["current"]["last_updated"]
    loc_tz_str=response["location"]["tz_id"]
    last_update = timezone_conv(last_upd_loc, loc_tz_str)
    humidity=response["current"]["humidity"]
    wind=response["current"]["wind_kph"]
    feelslike=response["current"]["feelslike_c"]


    return {
        "name": name,
        "country": country,
        "curr_temp_c": curr_temp_c,
        "curr_cond_icon": curr_cond_icon,
        "curr_cond_desc": curr_cond_desc,
        "last_update": last_update,
        "humidity": humidity,
        "wind": wind,
        "feelslike": feelslike,

    }

def get_city_info_hourly(city):
    api_key = "7ed79061f55449a1a76205741242401"
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=3"
    response = requests.get(url).json()  

    def target_days_list():
        local_timezone = pytz.timezone('Europe/Moscow')
        today = datetime.now(tz=local_timezone)
        tomorrow=today+ timedelta(days=1)
        after_tomorrow=today+ timedelta(days=2)

        today_str = today.strftime('%Y-%m-%d')
        tomorrow_str = tomorrow.strftime('%Y-%m-%d')
        after_tomorrow_str = after_tomorrow.strftime('%Y-%m-%d')

        target_days=[today_str,tomorrow_str,after_tomorrow_str]
        
        return target_days
    
    target_days=target_days_list()
    target_hours_list = ["03:00", "12:00", "21:00"]
    result= {}

    entry_dict = {}

    for i, day in enumerate(target_days):
        day_data = next((data for data in response['forecast']['forecastday'] if data['date'] == str(day)), None)

        if day_data:
            result[str(day)] = {
                'date': day,
                'hours': {}
            }
            for j, hour in enumerate(target_hours_list):
                date_hour = f"{day} {hour}"
                target_hour_data = next((time for time in day_data['hour'] if time['time'] == date_hour), None)
                #print(target_hour_data)

                if target_hour_data:
                    entry_data = {
                        f"temperature{i}{j}": target_hour_data['temp_c'],
                        f"text{i}{j}": target_hour_data['condition']['text'],
                        f"icon{i}{j}": target_hour_data['condition']['icon'],
                    }
                    entry_dict.update(entry_data)
                else:
                    print(f"No data found for {hour} on {day}")
        else:
            print(f"No data found for {day}")

    #print(entry_dict)
    return entry_dict


def get_city_info_days(city):
    api_key = "7ed79061f55449a1a76205741242401"
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=3"
    response = requests.get(url).json()  
    
    

    def target_days_list():
        local_timezone = pytz.timezone('Europe/Moscow')
        today = datetime.now(tz=local_timezone)
        tomorrow=today+ timedelta(days=1)
        after_tomorrow=today+ timedelta(days=2)

        today_str = today.strftime('%Y-%m-%d')
        tomorrow_str = tomorrow.strftime('%Y-%m-%d')
        after_tomorrow_str = after_tomorrow.strftime('%Y-%m-%d')

        target_days=[today_str,tomorrow_str,after_tomorrow_str]
        
        return target_days
    
    target_days=target_days_list()
    result = {}

    for i, target_day in enumerate(target_days):
        target_day_data = next((day for day in response['forecast']['forecastday'] if day['date'] == str(target_day)),None)
        target_day_dict = target_day_data.get('day', {})
        date_str=target_day_data["date"]
        date_obj=datetime.strptime(date_str, '%Y-%m-%d')
        formatted_date=date_obj.strftime('%d %b %a')

        if target_day_dict:
            result[f"max_temp_{i + 1}"] = target_day_dict["maxtemp_c"]
            result[f"min_temp_{i + 1}"] = target_day_dict["mintemp_c"]
            result[f"avg_temp_{i + 1}"] = target_day_dict["avgtemp_c"]
            result[f"rain_chance_{i + 1}"] = target_day_dict["daily_chance_of_rain"]
            result[f"avghumidity_{i + 1}"] = target_day_dict["avghumidity"]
            result[f"date_{i+1}"]=formatted_date
            result[f"text_{i + 1}"] = target_day_dict["condition"]["text"]
            result[f"icon_{i + 1}"] = target_day_dict["condition"]["icon"]
        
    return result


def home(request):
    cities = ["Istanbul", "London", "New York", "Madrid", "Rome", "Paris"]
    
    city_data = []
    for city in cities:
        city_info = get_city_info(city)
        city_info_days = get_city_info_days(city)
        city_info_hours = get_city_info_hourly(city)

        city_dict = {
            "city_info": city_info,
            "city_info_days": city_info_days,
            "city_info_hours": city_info_hours,
        }

        city_data.append(city_dict)

    context = {
        "city_data": city_data
    }

    return render(request, "weatherapp/home.html", context)

        

def search(request):
    if request.method == 'POST':
        city = request.POST.get('searched_city', '').strip()

        if city == "":
            error_message = 'Please enter a city before searching!'
            context = {
                "error_message": error_message,
            }
            return render(request, "weatherapp/search.html", context)

        else:
            try:
                city_info = get_city_info(city)
                city_info_days = get_city_info_days(city)
                city_info_hours = get_city_info_hourly(city)

                context = {
                    "city_info": city_info,
                    "city_info_days": city_info_days,
                    "city_info_hours": city_info_hours,
                    "city": city,
                }

                return render(request, "weatherapp/search.html", context)
            
            except KeyError as e:
                key_error= 'Please enter a valid city!'

                context = {
                    "key_error": key_error
                }

                return render(request, "weatherapp/search.html", context)

    return render(request, "weatherapp/search.html")
    

def mycity(request):
    try:
        city=request.user.my_city

        if city:
            city_info=get_city_info(city)
            city_info_days=get_city_info_days(city)
            city_info_hours=get_city_info_hourly(city)
                
            context={"city_info_days":city_info_days,
                    "city_info":city_info,
                    "city_info_hours": city_info_hours,
                    }
            return render(request, "weatherapp/mycity.html",context)
        
        else:
            raise ValueError("You do not have a registered city!")
        
    except ValueError as e:
        city_error= str(e)
        
        context= {
            "city_error": city_error
        }
        
        return render(request, "weatherapp/mycity.html",context)

    
def signup(request):
    if request.user.is_anonymous:
        if request.POST:
            form = SignUpForm(request.POST)
            if form.is_valid():
                try:
                    username=form.cleaned_data.get("username")
                    password=form.cleaned_data.get("password1")
                    form.save()
                    new_user=authenticate(username=username, password=password)
                    if new_user is not None:
                        login(request, new_user)
                        return redirect(reverse_lazy("weatherapp:home"))
                except Exception as e:
                    print(f"Error during sign-up: {e}")
            else:
                print(f"Form errors: {form.errors}")
        else:
            form = SignUpForm()

    else:
        return(redirect(reverse_lazy("weatherapp:home")))
    context = {"form": form}
    
    
    return render(request, "registration/signup.html", context)




        

        


    
    
    