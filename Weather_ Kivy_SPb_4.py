import requests
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView


def get_wind_direction(degree):
    directions = [
        (337.5, "Север"),
        (22.5, "Северо-восток"),
        (67.5, "Восток"),
        (112.5, "Юго-восток"),
        (157.5, "Юг"),
        (202.5, "Юго-запад"),
        (247.5, "Запад"),
        (292.5, "Северо-запад"),
    ]
    for threshold, direction in directions:
        if degree < threshold:
            return direction
    return directions[0][1]  # Вернуть "Север", если не найдено


def get_weather(city, api_key):
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&lang=ru"

    try:
        response = requests.get(base_url, timeout=30)
        response.raise_for_status()  # Проверка на наличие ошибок
        data = response.json()
        print(data)  # Вывод данных для отладки
        return data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Получение кода состояния
    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при получении данных: {e}")

    return None


def format_weather_data(weather_data):
    if weather_data is None:
        return "Ошибка: нет данных для отображения."

    temp = round(weather_data.get("main", {}).get("temp", 0) - 273.15)
    city = weather_data.get("name", "Неизвестный город")
    description = weather_data.get("weather", [{}])[0].get(
        "description", "Нет данных о погоде."
    )
    humidity = weather_data.get("main", {}).get("humidity", "Нет данных о влажности")
    wind_speed = weather_data.get("wind", {}).get(
        "speed", "Нет данных о скорости ветра"
    )
    wind_deg = weather_data.get("wind", {}).get("deg", None)
    wind_direction = (
        get_wind_direction(wind_deg)
        if wind_deg is not None
        else "Нет данных о направлении ветра"
    )

    return (
        f"Город: {city}\n"
        f"Температура: {temp} °C\n"
        f"Погода: {description}\n"
        f"Влажность: {humidity} %\n"
        f"Скорость ветра: {wind_speed} м/с\n"
        f"Направление ветра: {wind_direction}"
    )


class WeatherApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_key = "afb541e1af4ed79ffe4a5d73baf53203"  # Заменить на ваш API ключ
        self.city = "Санкт-Петербург"  # Установить город
        self.weather_data = get_weather(self.city, self.api_key)
        self.message = format_weather_data(self.weather_data)

    def build(self):
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
        scroll = ScrollView(
            size_hint=(1, None), size=(400, 600)
        )  # Установите фиксированные размеры
        label = Label(
            text=self.message,
            size_hint_y=None,
            height=len(self.message.splitlines()) * 40
            + 20,  # Увеличьте размер текста (высота)
            font_size="20sp",  # Увеличьте размер шрифта для видимости
            halign="center",  # Выравнивание по центру
            valign="middle",  # Вертикальное выравнивание по центру
            text_size=(400, None),
            padding=(20, 300),  # Добавьте отступы вокруг текста
        )
        label.bind(size=label.setter("size"))  # Динамическое изменение размера
        label.bind(texture_size=label.setter("size"))  # Применение к текстуре

        layout.add_widget(label)
        scroll.add_widget(layout)

        return scroll


if __name__ == "__main__":
    WeatherApp().run()
