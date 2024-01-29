
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, CityUpdate, PasswordUpdate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.template.response import TemplateResponse
from asgiref.sync import sync_to_async
from django.contrib import messages
import time
import asyncio
from .utils import (
    async_get_city_info,
    async_get_city_info_days,
    async_get_city_info_hourly,
)


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
            try:
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

            except:
                raise ValueError("You do not have a valid city, you can change it on the account tab!")

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
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password1")
                city=form.cleaned_data.get("my_city").title()
                form.cleaned_data["my_city"]=city
                form.save()
                new_user = authenticate(username=username, password=password)
                if new_user is not None:
                    login(request, new_user)
                    return redirect(reverse_lazy("weatherapp:home"))
            
            else:
                errors = list(form.errors.values())
                context = {
                    "form": form,
                    "errors": errors,
                    }
    
                return render(request, "registration/signup.html", context)
                
        else:
            form = SignUpForm()

    else:
        return redirect(reverse_lazy("weatherapp:home"))
    
    context = {"form": form}
    
    return render(request, "registration/signup.html", context)


@login_required
def chcity(request):
    city_form = CityUpdate()

    if request.method == 'POST':
        city_form = CityUpdate(request.POST, instance=request.user)
        if city_form.is_valid():
            city=city_form.cleaned_data.get("my_city").title()
            city_form.cleaned_data["my_city"]=city
            city_form.save()
            return redirect(reverse_lazy("weatherapp:mycity"))

    context = {"city_form": city_form}
    return render(request, "weatherapp/chcity.html", context)


@login_required
def chpassword(request):
    password_form = PasswordUpdate(user= request.user)

    if request.method == 'POST':
        password_form = PasswordUpdate(user= request.user, data=request.POST)
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, 'Your password was successfully changed.')


            return redirect(reverse_lazy("login"))
        
        else:
            errors = list(password_form.errors.values())

            context={
                "password_form": password_form,
                "errors": errors
            }
            return render(request, "registration/chpassword.html", context)

    
    context = {
        "password_form": password_form}
    return render(request, "registration/chpassword.html", context)
