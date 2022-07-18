import requests
import datetime
from config import open_weather_token


def get_weather(city, open_weather_token):
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
            )
        data = r.json()
        # pprint(data)

        city = data["name"]
        cur_weather = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        temp_min = data["main"]["temp_min"]
        wind = data["wind"]["speed"]
        sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

        print(f"Current time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
              f"\nWeather in {city}\nTemp: {cur_weather} Celsius\nHumidity: {humidity}%\nPressure: {pressure} mmHg"
              f"\nmin temp: {temp_min}\nWind: {wind} m/s\nSunrise time: {sunrise}\nSunset time: {sunset}"
              f"\nHave a good day ^_^")

    except Exception as ex:
        print(ex)
        print('please write name of a city again')


def main():
    city = input('in which city you want to check the weather? ')
    get_weather(city, open_weather_token)


if __name__ == '__main__':
    main()
