import requests


def get_wind_direction(degree):
    directions = [
        (0, "Север"),
        (22.5, "Северо-восток"),
        (67.5, "Восток"),
        (112.5, "Юго-восток"),
        (157.5, "Юг"),
        (202.5, "Юго-запад"),
        (247.5, "Запад"),
        (292.5, "Северо-запад"),
        (337.5, "Север"),
    ]
    for angle, direction in directions:
        if degree < angle:
            return direction
    return directions[0][1]  # Если больше 337.5, вернуть "Север"


def get_weather(city, api_key):
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&lang=ru"
    try:
        response = requests.get(base_url, timeout=30)
        response.raise_for_status()
        return response.json()  # Возвращаем json-данные напрямую
    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при получении данных: {e}")
        return None


def print_weather(weather_data):
    if weather_data is None:
        print("Ошибка: нет данных для отображения.")
        return

    # Выводим основные данные о погоде
    main_data = weather_data.get("main", {})
    wind_data = weather_data.get("wind", {})
    weather_desc = weather_data.get("weather", [{}])[0].get(
        "description", "Нет данных."
    )

    temperature_celsius = round(main_data.get("temp", 0) - 273.15)
    humidity = main_data.get("humidity", "Нет данных")
    wind_speed = wind_data.get("speed", "Нет данных")
    wind_direction = get_wind_direction(wind_data.get("deg", 0))

    print(f"Город: {weather_data.get('name', 'Нет данных.')}")
    print(f"Температура: {temperature_celsius} °C")
    print(f"Погода: {weather_desc}")
    print(f"Влажность: {humidity} %")
    print(f"Скорость ветра: {wind_speed} м/с")
    print(f"Направление ветра: {wind_direction}")


def main():
    api_key = "afb541e1af4ed79ffe4a5d73baf53203"  # API ключ
    city = input("Введите название города, для которого хотите узнать погоду: ")
    weather_data = get_weather(city, api_key)
    print_weather(weather_data)


if __name__ == "__main__":
    main()
