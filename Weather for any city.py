import requests
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


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


class WeatherApp(App):
    def build(self):
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        # Поле ввода для города
        self.city_input = TextInput(
            hint_text="Введите название города", size_hint_y=None, height=50
        )

        # Кнопка для получения погоды
        self.get_weather_button = Button(
            text="Получить погоду", size_hint_y=None, height=50
        )
        self.get_weather_button.bind(on_press=self.show_weather)

        # Добавляем виджеты на макет
        self.layout.add_widget(self.city_input)
        self.layout.add_widget(self.get_weather_button)

        # Метка для отображения данных о погоде
        self.label = Label(
            text="",
            size_hint_y=None,
            height=500,
            font_size="20sp",
            halign="center",
            valign="middle",
            text_size=(380, None),
            padding=(20, 300),
        )
        self.label.bind(size=self.label.setter("size"))
        self.layout.add_widget(self.label)

        return self.layout

    def get_weather(self, city, api_key="afb541e1af4ed79ffe4a5d73baf53203"):
        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&lang=ru"
        try:
            response = requests.get(base_url, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Произошла ошибка при получении данных: {e}")
            return None

    def show_weather(self, instance):
        city = self.city_input.text.strip()
        if not city:
            self.label.text = "Пожалуйста, введите название города."
            return

        weather_data = self.get_weather(city)
        if weather_data is None:
            self.label.text = "Ошибка: нет данных для отображения."
            return

        # Обработка данных о погоде
        main_data = weather_data.get("main", {})
        wind_data = weather_data.get("wind", {})
        weather_desc = weather_data.get("weather", [{}])[0].get(
            "description", "Нет данных."
        )

        temperature_celsius = round(main_data.get("temp", 0) - 273.15)
        humidity = main_data.get("humidity", "Нет данных")
        wind_speed = wind_data.get("speed", "Нет данных")
        wind_direction = get_wind_direction(wind_data.get("deg", 0))

        message = (
            f"Город: {weather_data.get('name', 'Нет данных.')}\n"
            f"Температура: {temperature_celsius} °C\n"
            f"Погода: {weather_desc}\n"
            f"Влажность: {humidity} %\n"
            f"Скорость ветра: {wind_speed} м/с\n"
            f"Направление ветра: {wind_direction}"
        )

        self.label.text = message


if __name__ == "__main__":
    WeatherApp().run()
