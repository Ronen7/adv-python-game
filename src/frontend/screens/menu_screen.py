from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from src.backend.data_management import DataManagement

font1_path = 'assets/fonts/Arcade1.TTF'
font2_path = 'assets/fonts/Arcade2.ttf'


class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)
        self.data_management = DataManagement()
        layout = BoxLayout(orientation='vertical', padding=10)

        layout.add_widget(Widget(size_hint_y=0.3))

        game_name = Label(text='MEMORY GAME',
                          size_hint_y=0.01,
                          font_name=font1_path,
                          font_size=65)
        game_name.color = (0, 0, 0, 1)
        layout.add_widget(game_name)

        layout.add_widget(Widget(size_hint_y=0.03))

        progress_bar = ProgressBar(
            max=100,
            size_hint=(1, 0.1),
            pos_hint={'center_x': 0.5},
        )
        layout.add_widget(progress_bar)

        layout.add_widget(Widget(size_hint_y=0.2))

        button_info = Button(
            text='Info',
            size_hint=(0.7, 0.3),
            background_color=(0.7, 0.7, 0.7, 1),
            color=(0, 0, 0, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            font_name=font1_path,
            font_size=40,
            on_press=self.show_info
        )
        layout.add_widget(button_info)

        with button_info.canvas.before:
            Color(0., 0., 0., 1)
            setattr(button_info, 'border_line', Line(width=10))

        button_info.bind(pos=lambda instance, value: self.update_rect(instance),
                         size=lambda instance, value: self.update_rect(instance))
        button_info.background_normal = ''
        button_info.background_down = ''

        self.highscores_label = Label(
            font_size=28,
            color=(0, 0, 0, 1),
            markup=True,
            font_name=font2_path,
        )
        layout.add_widget(self.highscores_label)

        self.update_high_scores_display()

        self.player_name_input = TextInput(
            hint_text='ENTER  PLAYER  NAME',
            hint_text_color=(0, 0, 0, 1),
            multiline=False,
            font_size=35,
            font_name=font1_path,
            size_hint=(0.9, 0.15),
            background_color=(0.7, 0.7, 0.7, 1),
            foreground_color=(0, 0, 0, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            halign='center',
            padding_y=(10, 10),
        )
        layout.add_widget(self.player_name_input)

        layout.add_widget(Widget(size_hint_y=0.2))

        button_play = Button(
            text='Start game',
            size_hint=(0.7, 0.3),
            background_color=(0.7, 0.7, 0.7, 1),
            color=(0, 0, 0, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            font_name=font1_path,
            font_size=40,
        )

        with button_play.canvas.before:
            Color(0, 0, 0, 1)
            setattr(button_play, 'border_line', Line(width=10))

        button_play.bind(pos=lambda instance, value: self.update_rect(instance),
                         size=lambda instance, value: self.update_rect(instance))
        button_play.background_normal = ''
        button_play.background_down = ''

        button_play.bind(on_press=self.start_game)
        layout.add_widget(button_play)

        layout.add_widget(Widget(size_hint_y=0.5))

        self.add_widget(layout)

        self.load_high_scores()

    def show_info(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        info_label = Label(
            text="Welcome to the Memory Game! This game tests and improves your memory skills.\n\n"
                 "You will be presented with a grid of tiles, some of which will momentarily change color. "
                 "Remember the colored tiles! Once they revert to their original color, it's your turn "
                 "to tap them in the same sequence.\n\n"
                 "As you progress, the game becomes more challenging "
                 "by increasing the grid size and changing the number of colored tiles. "
                 "Can you keep up as the difficulty rises? Good luck!",
            font_size=20,
            font_name='Impact',
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            text_size=(380, None),
            halign='left',
            valign='top')
        info_label.bind(texture_size=info_label.setter('size'))

        content.add_widget(info_label)

        popup = Popup(
            title='Game Information',
            title_align='center',
            title_color=(1, 1, 1, 1),
            title_font=font2_path,
            title_size=25,
            separator_color=(0.7, 0.7, 0.7, 1),
            content=content,
            size_hint=(None, None),
            size=(450, 450),
            auto_dismiss=True
        )

        with popup.canvas.before:
            Color(1, 1, 1)
            border_width = 2
            Line(rectangle=(popup.x, popup.y, popup.width, popup.height), width=border_width)

        popup.open()

    # RACE START

    def start_game(self, instance):
        self.manager.current = 'game'

    def update_rect(self, instance):
        instance.border_line.rectangle = (
            instance.x,
            instance.y,
            instance.width,
            instance.height,
        )

    def load_high_scores(self):
        self.data_management.load_high_score()

    def update_high_scores_display(self):
        high_scores = self.data_management.load_high_score()
        top_scores = high_scores[:3]
        self.highscores_label.text = '[b][u]HIGHSCORES[/u][/b]\n' + '\n'.join(
            [f"{i + 1}. {score[0]} - {score[1]}" for i, score in enumerate(top_scores)]
        )

    def on_enter(self, *args):
        self.update_high_scores_display()
