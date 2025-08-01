from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window

Window.size = (300, 390)

class BotaoArredondado(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = [0, 0, 0, 0]  # Transparente para usar canvas
        self.color = (1, 1, 1, 1)  # Texto branco

        with self.canvas.before:
            Color(0.18, 0.60, 0.68, 1)  # Azul petróleo moderno
            self.rect = RoundedRectangle(radius=[20], pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class MainApp(App):
    def build(self):
        self.operators = ['/', '*', '+', '-']
        self.last_was_operator = None
        self.last_button = None

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.solution = TextInput(
            multiline=False, readonly=True, halign='right', font_size=40
        )
        main_layout.add_widget(self.solution)

        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['.', '0', 'C', '+'],
        ]

        for row in buttons:
            h_layout = BoxLayout(spacing=10)
            for label in row:
                button = BotaoArredondado(
                    text=label,
                    size_hint=(1, 1),
                )
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)

        equals_button = BotaoArredondado(
            text='=',
            size_hint=(1, 1)
        )
        equals_button.bind(on_press=self.on_solution)
        main_layout.add_widget(equals_button)

        return main_layout

    def on_button_press(self, instance):
        current = self.solution.text
        button_text = instance.text

        if button_text == 'C':
            self.solution.text = ''
        else:
            if current and (
                self.last_was_operator and button_text in self.operators):
                return
            elif current == '' and button_text in self.operators:
                return
            else:
                new_text = current + button_text
                self.solution.text = new_text

        self.last_button = button_text
        self.last_was_operator = self.last_button in self.operators

    def on_solution(self, instance):
        text = self.solution.text
        if text:
            try:
                solution = str(eval(text))
                self.solution.text = solution
            except Exception:
                self.solution.text = 'Erro'

if __name__ == '__main__':
    MainApp().run()
