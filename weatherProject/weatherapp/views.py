from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate 
from .forms import SignUpForm
from .utils import get_city_info, get_city_info_days, get_city_info_hourly
import asyncio
from django.template.response import TemplateResponse
import time



async def async_get_city_info(city):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: get_city_info(city))

async def async_get_city_info_days(city):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: get_city_info_days(city))

async def async_get_city_info_hourly(city):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: get_city_info_hourly(city))


async def home(request):
    st= time.time()

    cities = ["Istanbul", "London", "New York", "Madrid", "Rome", "Paris"]
    
    city_data = []

    tasks_info = [async_get_city_info(city) for city in cities]
    tasks_days = [async_get_city_info_days(city) for city in cities]
    tasks_hourly = [async_get_city_info_hourly(city) for city in cities]

    results_info = await asyncio.gather(*tasks_info)
    results_days = await asyncio.gather(*tasks_days)
    results_hourly = await asyncio.gather(*tasks_hourly)

    for  info, days, hourly in zip( results_info, results_days, results_hourly):
        city_dict = {
            "city_info": info,
            "city_info_days": days,
            "city_info_hours": hourly,
        }
        city_data.append(city_dict)

    context = {
        "city_data": city_data
    }

    et= time.time()
    elap_time=et-st
    print(elap_time)
    return  TemplateResponse(request, "weatherapp/home.html", context)


        

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




        

        


    
    
    