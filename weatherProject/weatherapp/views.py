from django.shortcuts import render
from django.urls import reverse
import requests
from .models import City
import pytz
from pytz import timezone
from datetime import datetime


# Create your views here.
def get_city_info(city):
    api_key = "7ed79061f55449a1a76205741242401"
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    response = requests.get(url).json()
    print(response)    

    name = response["location"]["name"]
    curr_temp_c = round(response["current"]["temp_c"])
    curr_cond_icon = response["current"]["condition"]["icon"]
    curr_cond_desc = response["current"]["condition"]["text"]
    last_upd_loc = response["current"]["last_updated"]
    loc_tz_str=response["location"]["tz_id"]
    last_update = timezone_conv(last_upd_loc, loc_tz_str)

    return {
        "name": name,
        "curr_temp_c": curr_temp_c,
        "curr_cond_icon": curr_cond_icon,
        "curr_cond_desc": curr_cond_desc,
        "last_update": last_update,
    }


def timezone_conv(last_upd_loc, loc_tz_str):
    date_format = '%Y-%m-%d %H:%M'
    last_upd_dt = datetime.strptime(last_upd_loc, date_format)

    loc_tz = pytz.timezone(loc_tz_str)
    last_upd_dt_loc = loc_tz.localize(last_upd_dt)

    new_tz = pytz.timezone('Europe/Moscow')
    last_update = last_upd_dt_loc.astimezone(new_tz)
    last_update_conv_str = last_update.strftime(date_format)

    return last_update_conv_str


def grid(request):
    cities = ["Istanbul", "London", "New York", "Tokyo", "Sydney", "Paris"]
    
    city_data = []
    for city in cities:
        city_info = get_city_info(city)
        city_data.append(city_info)

    context = {
        "city_data": city_data,
    }

    return render(request, "weatherapp/grid.html", context)
        

def search(request):
        city=request.POST.get("searched_city")

        city_info=get_city_info(city)
        
        context={"city_info":city_info,
               }
        return render(request, "weatherapp/search.html",context)
        

        


    
    
    