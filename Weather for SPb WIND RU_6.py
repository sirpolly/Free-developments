import requests


def get_wind_direction(degree):
    if degree >= 337.5 or degree < 22.5:
        return "Север"
    elif 22.5 <= degree < 67.5:
        return "Северо-восток"
    elif 67.5 <= degree < 112.5:
        return "Восток"
    elif 112.5 <= degree < 157.5:
        return "Юго-восток"
    elif 157.5 <= degree < 202.5:
        return "Юг"
    elif 202.5 <= degree < 247.5:
        return "Юго-запад"
    elif 247.5 <= degree < 292.5:
        return "Запад"
    elif 292.5 <= degree < 337.5:
        return "Северо-запад"


def get_weather(city, api_key):
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&lang=ru"
    try:
        response = requests.get(base_url, timeout=30)
        response.raise_for_status()  # это вызовет исключение для HTTP ошибок
    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при получении данных: {e}")
        return None  # возвращаем None в случае ошибки
    weather_data = response.json()
    return weather_data


def print_weather(weather_data):
    if weather_data is None:
        print("Ошибка: нет данных для отображения.")
        return
    if "main" in weather_data and "temp" in weather_data["main"]:
        # Конвертация температуры из Кельвинов в Цельсий и округление до целого числа
        temperature_celsius = round(weather_data["main"]["temp"] - 273.15)
        print(f"Температура: {temperature_celsius} °C")  # Теперь без десятых и сотых
    else:
        print("Ошибка: Не удалось получить данные о температуре.")
    if "name" in weather_data:
        print(f"Город: {weather_data['name']}")
    else:
        print("Ошибка: Не удалось получить название города.")
    if "weather" in weather_data and len(weather_data["weather"]) > 0:
        print(f"Погода: {weather_data['weather'][0]['description']}")
    else:
        print("Ошибка: Не удалось получить данные о погоде.")
    if "main" in weather_data and "humidity" in weather_data["main"]:
        print(f"Влажность: {weather_data['main']['humidity']} %")
    else:
        print("Ошибка: Не удалось получить данные о влажности.")
    if "wind" in weather_data:
        if "speed" in weather_data["wind"]:
            print(f"Скорость ветра: {weather_data['wind']['speed']} м/с")
        else:
            print("Ошибка: Не удалось получить данные о скорости ветра.")
        if "deg" in weather_data["wind"]:
            wind_deg = weather_data["wind"]["deg"]
            wind_direction = get_wind_direction(
                wind_deg
            )  # Убедитесь, что функция доступна
            print(f"Направление ветра: {wind_direction}")
        else:
            print("Ошибка: Не удалось получить данные о направлении ветра.")
    else:
        print("Ошибка: Не удалось получить данные о ветре.")


def main():
    api_key = "afb541e1af4ed79ffe4a5d73baf53203"  # Замените на ваш API ключ
    city = "Санкт-Петербург"  # Установите город на Санкт-Петербург
    weather_data = get_weather(city, api_key)
    print_weather(weather_data)


if __name__ == "__main__":
    main()
    
