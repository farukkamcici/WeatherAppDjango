
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from .utils import (
    async_get_city_info,
    async_get_city_info_days,
    async_get_city_info_hourly,
)
from django.template.response import TemplateResponse
import time
import asyncio
from asgiref.sync import sync_to_async


async def home(request):
    st = time.time()

    cities = ["Istanbul", "London", "New York", "Madrid", "Rome", "Paris"]

    city_data = []

    tasks_info = [await async_get_city_info(city) for city in cities]
    tasks_days = [async_get_city_info_days(city) for city in cities]
    tasks_hourly = [async_get_city_info_hourly(city) for city in cities]

    results_info = await asyncio.gather(*tasks_info)
    results_days = await asyncio.gather(*tasks_days)
    results_hourly = await asyncio.gather(*tasks_hourly)

    for info, days, hourly in zip(results_info, results_days, results_hourly):
        city_dict = {
            "city_info": info,
            "city_info_days": days,
            "city_info_hours": hourly,
        }
        city_data.append(city_dict)

    context = {
        "city_data": city_data
    }

    et = time.time()
    elap_time = et - st
    print(elap_time)
    return TemplateResponse(request, "weatherapp/home.html", context)


async def search(request):
    if request.method == 'POST':
        city = request.POST.get('searched_city', '').strip()

        if city == "":
            error_message = 'Please enter a city before searching!'
            context = {"error_message": error_message}
            return TemplateResponse(request, "weatherapp/search.html", context)

        else:
            try:
                tasks_info = [await async_get_city_info(city)]
                tasks_days = [async_get_city_info_days(city)]
                tasks_hourly = [async_get_city_info_hourly(city)]

                results_info = await asyncio.gather(*tasks_info)
                results_days = await asyncio.gather(*tasks_days)
                results_hourly = await asyncio.gather(*tasks_hourly)

                cities_data = {}
                for info, days, hourly in zip(results_info, results_days, results_hourly):
                    city_data = {
                        "city_info": info,
                        "city_info_days": days,
                        "city_info_hours": hourly,
                    }
                    cities_data["city_data"]= city_data

                context = {
                    "cities_data": cities_data,
                }

                return TemplateResponse(request, "weatherapp/search.html", context)
            
            except KeyError as e:
                key_error = 'Please enter a valid city!'
                context = {"key_error": key_error}
                return TemplateResponse(request, "weatherapp/search.html", context)

    return TemplateResponse(request, "weatherapp/search.html")



@sync_to_async
def get_user_city(request):
    return request.user.my_city

async def mycity(request):
    try:
        city = await get_user_city(request)


        if city:
            tasks_info = [await async_get_city_info(city)]
            tasks_days = [async_get_city_info_days(city)]
            tasks_hourly = [async_get_city_info_hourly(city)]

            results_info = await asyncio.gather(*tasks_info)
            results_days = await asyncio.gather(*tasks_days)
            results_hourly = await asyncio.gather(*tasks_hourly)

            for info, days, hourly in zip(results_info, results_days, results_hourly):
                context = {
                    "city_info": info,
                    "city_info_days": days,
                    "city_info_hours": hourly,
                }
                return TemplateResponse(request, "weatherapp/mycity.html", context)

        else:
            raise ValueError("You do not have a registered city!")

    except ValueError as e:
        city_error = str(e)

        context = {
            "city_error": city_error
        }

        return TemplateResponse(request, "weatherapp/mycity.html", context)


def signup(request):
    if request.user.is_anonymous:
        if request.POST:
            form = SignUpForm(request.POST)
            if form.is_valid():
                try:
                    username = form.cleaned_data.get("username")
                    password = form.cleaned_data.get("password1")
                    form.save()
                    new_user = authenticate(username=username, password=password)
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
        return redirect(reverse_lazy("weatherapp:home"))
    
    context = {"form": form}
    
    return render(request, "registration/signup.html", context)
