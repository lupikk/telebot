import datetime
import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher  # Класс, который улавливает сообщения, и на него прописываются реакции
from aiogram.utils import executor  # вывод бота в онлайн
from config import tg_token_bot, open_weather_token

bot = Bot(token=tg_token_bot)  # токен
dp = Dispatcher(bot)  # диспетчер


@dp.message_handler(commands=['start', 'help'])  # Декоратор события в чате
async def commands_start(message: types.Message):
    await message.reply(
        "Hi! I'm a weather tracking bot. Write the name of the city and I will send you information")  # ответ


@dp.message_handler()
async def get_weather(message: types.Message):
    try:
        smile = {
            'Clear': 'Clear \U0001F31E',
            'Clouds': 'Cloudy \U0001F325',
            'Rain': 'Rain \U0001F327',
            'Drizzle': 'Rain \U0001F327',
            'Thunderstorm': 'Thunderstorm \U0001F329',
            'Snow': 'Snow \U0001F328',
            'Mist': 'Mist \U0001F32B'
        }
        h = requests.get(
            f'http://api.openweathermap.org/data/2.5/forecast?q={message.text}&appid={open_weather_token}&units'
            f'=metric&lang=ua '
        )
        data_weather = h.json()
        city = data_weather['city']['name']
        cut_weather = data_weather['list'][0]['main']['temp']
        weather_des = data_weather['list'][1]['weather'][0]['main']
        if weather_des in smile:
            wd = smile[weather_des]
        else:
            wd = 'Визерни у вікно, я не розумію що там коїться'
        feel_temp = data_weather['list'][0]['main']['feels_like']
        pressure = data_weather['list'][0]['main']['pressure']
        humidity = data_weather['list'][0]['main']['humidity']
        precipitation = data_weather['list'][0]['pop']
        wind = data_weather['list'][0]['wind']['speed']
        message_wind = ''
        if wind > 10.8:
            message_wind = '. Будь обережним на вулиці, вітер сильний'
        elif wind < 10.8:
            pass
        messag_atent = 'Have a nice day \U0001F609'
        if weather_des == 'Rain' or weather_des == 'Drizzle':
            messag_atent = 'Take an umbrella \U00002614'
        elif weather_des == 'Thunderstorm':
            messag_atent = 'It is better to stay at home ' \
                           '\U0001F329'
        elif weather_des == 'Snow':
            messag_atent = 'Be careful on the street \U00002744'
        elif weather_des == 'Mist':
            messag_atent = 'Be careful while driving \U0001F301'
        await message.reply(f'Current time {datetime.datetime.now().strftime("%d-%m-%Y %H:%M")}\n'
                            f'Weather in {city}:\nTemperature: {cut_weather}°C, feels like: {feel_temp}°C\n{wd}\n'
                            f'Atmospheric pressure: {pressure} mm Hg\nRelative humidity: {humidity}%\nChance of '
                            f'precipitation for today: {precipitation * 100}%\nWind speed: {wind} m/s '
                            f'{message_wind}\n{messag_atent}')
        await message.answer('Enter the name of the city:')

    except:
        await message.reply('\U0000203C Check the city name \U0000203C')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
