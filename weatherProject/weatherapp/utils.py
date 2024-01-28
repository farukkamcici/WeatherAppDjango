import pytz
from datetime import datetime, timedelta
import aiohttp
import asyncio

async def async_get_city_info(city):
    api_key = "7ed79061f55449a1a76205741242401"
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as data:
            response = await data.json()

    return extract_city_info(response)

async def async_get_city_info_days(city):
    api_key = "7ed79061f55449a1a76205741242401"
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=3"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as data:
            response = await data.json()

    return extract_city_info_days(response)

async def async_get_city_info_hourly(city):
    api_key = "7ed79061f55449a1a76205741242401"
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=3"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as data:
            response = await data.json()

    return extract_city_info_hourly(response)

async def timezone_conv(last_upd_loc, loc_tz_str):
    date_format = '%Y-%m-%d %H:%M'
    last_upd_dt = datetime.strptime(last_upd_loc, date_format)

    loc_tz = pytz.timezone(loc_tz_str)
    last_upd_dt_loc = loc_tz.localize(last_upd_dt)

    new_tz = pytz.timezone('Europe/Moscow')
    last_update = last_upd_dt_loc.astimezone(new_tz)
    last_update_conv_str = last_update.strftime(date_format)

    return last_update_conv_str

async def extract_city_info(response):
    name = response["location"]["name"]
    country = response["location"]["country"]
    curr_temp_c = round(response["current"]["temp_c"])
    curr_cond_icon = response["current"]["condition"]["icon"]
    curr_cond_desc = response["current"]["condition"]["text"]
    last_upd_loc = response["current"]["last_updated"]
    loc_tz_str = response["location"]["tz_id"]
    last_update = await timezone_conv(last_upd_loc, loc_tz_str)
    humidity = response["current"]["humidity"]
    wind = response["current"]["wind_kph"]
    feelslike = response["current"]["feelslike_c"]

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

def extract_city_info_hourly(response):
    target_days = target_days_list()

    target_hours_list = ["03:00", "12:00", "21:00"]
    result = {}
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

    return entry_dict

def extract_city_info_days(response):
    target_days = target_days_list()
    result = {}

    for i, target_day in enumerate(target_days):
        target_day_data = next((day for day in response['forecast']['forecastday'] if day['date'] == str(target_day)), None)
        target_day_dict = target_day_data.get('day', {})
        date_str = target_day_data["date"]
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        formatted_date = date_obj.strftime('%d %b %a')

        if target_day_dict:
            result[f"max_temp_{i + 1}"] = target_day_dict["maxtemp_c"]
            result[f"min_temp_{i + 1}"] = target_day_dict["mintemp_c"]
            result[f"avg_temp_{i + 1}"] = target_day_dict["avgtemp_c"]
            result[f"rain_chance_{i + 1}"] = target_day_dict["daily_chance_of_rain"]
            result[f"avghumidity_{i + 1}"] = target_day_dict["avghumidity"]
            result[f"date_{i+1}"] = formatted_date
            result[f"text_{i + 1}"] = target_day_dict["condition"]["text"]
            result[f"icon_{i + 1}"] = target_day_dict["condition"]["icon"]

    return result

def target_days_list():
    local_timezone = pytz.timezone('Europe/Moscow')
    today = datetime.now(tz=local_timezone)
    tomorrow = today + timedelta(days=1)
    after_tomorrow = today + timedelta(days=2)

    today_str = today.strftime('%Y-%m-%d')
    tomorrow_str = tomorrow.strftime('%Y-%m-%d')
    after_tomorrow_str = after_tomorrow.strftime('%Y-%m-%d')

    target_days = [today_str, tomorrow_str, after_tomorrow_str]

    return target_days
