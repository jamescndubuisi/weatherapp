from django.shortcuts import render
import requests
import datetime


def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()
    print(response)
    # error_exists = None
    if response['cod'] != 200:
        error_exists = True
        return {}, [], error_exists
    else:
        lat, lon = response['coord']['lat'], response['coord']['lon']
        count = 5
        units = "metric"
        forecast_response = requests.get(forecast_url.format(lat, lon,  api_key, count, units)).json()
        # print(forecast_response)

        weather_data = {
            'city': city,
            'temperature': round(response['main']['temp'] - 273.15, 2),
            'description': response['weather'][0]['description'],
            'icon': response['weather'][0]['icon'],
        }

        daily_forecasts = []
        for daily_data in forecast_response['list'][:5]:
            # print(daily_data)
            data = daily_data["main"]
            # print(data)
            daily_forecasts.append({
                'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
                'hour': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%I'),
                'minutes': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%M'),
                'ampm': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%p'),
                'min_temp': round(data['temp_min'], 2),
                'max_temp': round(data['temp_max'], 2),
                'description': daily_data['weather'][0]['description'],
                'icon': daily_data['weather'][0]['icon'],
            })
        # print(daily_forecasts)
        error_exists = False
    return weather_data, daily_forecasts, error_exists


def index(request):
    # api_key = '1ebfba407737f1180cd073f9fad8abf0'
    api_key = "7c6aa4f298cb2c7cf6bf194393331ff2"
    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    forecast_url = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}&cnt={}&units={}'
    # forecast_url = 'https://api.openweathermap.org/data/2.5/forecast/daily?lat={}&lon={}&cnt={}&appid={}'

    if request.method == 'POST':
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None)

        weather_data1, daily_forecasts1, error_exists1 = fetch_weather_and_forecast(city1, api_key, current_weather_url, forecast_url)

        if city2:
            weather_data2, daily_forecasts2, error_exists2 = fetch_weather_and_forecast(city2, api_key, current_weather_url,
                                                                         forecast_url)
        else:
            weather_data2, daily_forecasts2, error_exists2 = None, None, None

        context = {
            'weather_data1': weather_data1,
            'daily_forecasts1': daily_forecasts1,
            "first_city": city1,
            "error_exists1": error_exists1,
            'weather_data2': weather_data2,
            'daily_forecasts2': daily_forecasts2,
            "second_city": city2,
            "error_exists2": error_exists2,
        }

        return render(request, 'weather_app/index.html', context)
    else:
        return render(request, 'weather_app/index.html')

