import requests
import json
from datetime import datetime
import smtplib
from email.header import Header
from email.mime.text import MIMEText

mode = int(input('Выберете режим работы:\n1 - проверка на дождь\n2 - отправить погоду\n'))

my_email = ''
my_password = ''
adr_mail = ''

api_key = ""
url = 'https://api.openweathermap.org/data/2.5/weather'
url_2 = 'https://api.openweathermap.org/data/2.5/forecast'
MY_LAT = 55.53
MY_LON = 37.52
params = {
    "lat": MY_LAT,
    "lon": MY_LON,
    "appid": api_key,
    "lang": "ru",
    "units": "metric",
    "cnt": 7
}
time_format = "%y-%m-%d %H:%M:%S"
will_rain = False


if mode == 1:
    subject = '☂Возьми зонтик☂'
    # --------Получение погоды на сегодня-------- #
    response = requests.get(url=url, params=params)
    response.raise_for_status()

    data = response.json()

    with open('weather_now.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    weather = data["weather"][0]["description"].capitalize()
    temp = data["main"]["temp"]
    wind_speed = data["wind"]["speed"]
    region_name = data["name"]
    dt = datetime.now()
    time = str(dt.replace(microsecond=0, tzinfo=None))
    time_new = time[8:10] + '-' + time[5:7] + '-' + time[:4] + ' ' + time[11:]

    weather_info = f"\nКоротко о погоде на {time_new}:"
    region_info = f'\nРайон: {region_name}'
    clouds_info = f'\nОблачность: {weather}'
    temp_info = f'\nТемпература: {temp}°C'
    wind_speed_info = f'\nСкорость ветра: {wind_speed} м/с'

    # --------Получение погоды на ближайшие 18 часов-------- #
    response = requests.get(url=url_2, params=params)
    response.raise_for_status()

    data = response.json()

    with open('weather_forecast.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    data_slice = data["list"][:7]

    for hour_data in data_slice:
        weather = hour_data['weather'][0]
        weather_id = hour_data['weather'][0]['id']
        if int(weather_id) < 700:
            will_rain = True

    if will_rain:
        text_if_rainy = 'Не забудь взять зонтик! Сегодня может быть дождь!\n' + weather_info + region_info + clouds_info + temp_info + wind_speed_info
        mime = MIMEText(text_if_rainy, 'plain', 'utf-8')
        mime['Subject'] = Header(subject, 'utf-8')

        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(user=my_email, password=my_password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=adr_mail,
                msg=mime.as_string()
            )
    else:
        print('Осадков не ожидается!')

elif mode == 2:
    subject = 'Погода на сегодня!'

    response = requests.get(url=url, params=params)
    response.raise_for_status()

    data = response.json()

    with open('weather_now.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    weather = data["weather"][0]["description"].capitalize()
    temp = data["main"]["temp"]
    wind_speed = data["wind"]["speed"]
    region_name = data["name"]
    dt = datetime.now()
    time = str(dt.replace(microsecond=0, tzinfo=None))
    time_new = time[8:10] + '-' + time[5:7] + '-' + time[:4] + ' ' + time[11:]

    weather_info = f"\nКоротко о погоде на {time_new}:"
    region_info = f'\nРайон: {region_name}'
    clouds_info = f'\nОблачность: {weather}'
    temp_info = f'\nТемпература: {temp}°C'
    wind_speed_info = f'\nСкорость ветра: {wind_speed} м/с'

    text_with_weather = f'{weather_info}{region_info}{clouds_info}{temp_info}{wind_speed_info}'
    mime = MIMEText(text_with_weather, 'plain', 'utf-8')
    mime['Subject'] = Header(subject, 'utf-8')

    with smtplib.SMTP('smtp.gmail.com') as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=adr_mail,
            msg=mime.as_string()
        )

else:
    print('Неверно выбран режим работы!')
