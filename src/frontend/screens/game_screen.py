from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from kivy.clock import Clock
import sys
sys.path.append('/Path/to/adv-python-game-main')
from src.backend.game_logic import GameLogic
from src.backend.data_management import DataManagement

font1_path = 'assets/fonts/Arcade1.TTF'
font2_path = 'assets/fonts/Arcade2.ttf'


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.game_logic = GameLogic()
        self.data_management = DataManagement()
        self.layout = BoxLayout(orientation='vertical')

        self.grid = GridLayout(cols=self.game_logic.cols, spacing=2, size_hint=(1, 0.8))
        with self.grid.canvas.before:
            Color(1, 1, 1, 1)
            self.bg = Rectangle(size=(self.grid.width - self.grid.spacing[0] * 2,
                                      self.grid.height - self.grid.spacing[1] * 2),
                                pos=self.grid.pos)

        for i in range(self.game_logic.cols * self.game_logic.cols):
            tile = Button(background_color=(1, 1, 1, 1))
            tile.bind(on_press=self.check_tile)
            self.grid.add_widget(tile)
        self.layout.add_widget(self.grid)

        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        back_button = Button(
            text='Main Menu',
            size_hint=(0.5, 1),
            font_name=font2_path,
            font_size=30,
        )
        back_button.bind(on_press=self.go_to_menu)

        button_layout.add_widget(back_button)

        labels_layout = BoxLayout(orientation='vertical', size_hint=(0.5, 1))

        self.points_label = Label(
            text=f'Points: {self.game_logic.points}',
            size_hint=(1, 0.5),
            color=(0, 0, 0, 1),
            font_name=font2_path,
        )
        labels_layout.add_widget(self.points_label)

        self.lives_label = Label(
            text=f'Lives: {self.game_logic.lives}',
            size_hint=(1, 0.5),
            color=(0, 0, 0, 1),
            font_name=font2_path,
        )
        labels_layout.add_widget(self.lives_label)

        button_layout.add_widget(labels_layout)
        self.layout.add_widget(button_layout)
        self.add_widget(self.layout)

        self.lost_popup = Popup(
            title='Oh no...You Lost!',
            title_align='center',
            title_font=font2_path,
            title_size=28,
            separator_height=0,
            size_hint=(None, None),
            size=(400, 350),
            auto_dismiss=False
        )

        popup_lost_content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self.player_name_label = Label(font_size=20, font_name=font2_path, )
        self.player_score_label = Label(font_size=20, font_name=font2_path, )
        popup_lost_content.add_widget(self.player_name_label)
        popup_lost_content.add_widget(self.player_score_label)

        restart_button = Button(
            text='Restart Game',
            background_color=(1, 1, 1, 1),
            color=(0, 0, 0, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            font_name=font2_path,
            font_size=20,
            on_press=self.start_game
        )

        menu_button = Button(
            text='Go to Menu',
            background_color=(1, 1, 1, 1),
            color=(0, 0, 0, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            font_name=font2_path,
            font_size=20,
            on_press=self.go_to_menu
        )

        popup_lost_content.add_widget(restart_button)
        popup_lost_content.add_widget(menu_button)

        self.lost_popup.content = popup_lost_content

        self.update_grid_layout()

    def update_grid_layout(self):
        self.grid.cols = self.game_logic.cols
        self.grid.clear_widgets()
        buttons = []
        for i in range(self.game_logic.cols * self.game_logic.cols):
            tile = Button(background_color=(1, 1, 1, 1))
            tile.bind(on_press=self.check_tile)
            self.grid.add_widget(tile)
            buttons.append(tile)
        self.game_logic.set_buttons(buttons)

    def check_tile(self, instance):
        tile_index = len(self.grid.children) - 1 - self.grid.children.index(instance)
        result = self.game_logic.check_tile(tile_index)
        if result['status'] == 'correct':
            instance.background_color = (1, 0, 1, 1)
            self.check_sequence_completion()
            self.game_logic.hide_sequence()
        elif result['status'] == 'wrong':
            if self.game_logic.scheduled_event:
                Clock.unschedule(self.game_logic.scheduled_event)
                self.game_logic.scheduled_event = None
            for i in range(self.game_logic.cols*self.game_logic.cols):
                self.grid.children[len(self.grid.children) - 1 - i].background_color = (1, 1, 1, 1)
            instance.background_color = (1, 0, 0, 1)
            Clock.schedule_once(lambda dt: self.start_new_sequence(), 1)
        elif result['status'] == 'double_click':
            instance.background_color = (1, 1, 1, 1)

    def check_sequence_completion(self):
        result = self.game_logic.check_sequence()
        if result['status'] == 'correct':
            for i in self.game_logic.sequence_check:
                self.grid.children[len(self.grid.children) - 1 - i].background_color = (0, 1, 0, 1)
            Clock.schedule_once(lambda dt: self.start_new_sequence(), 1)

    def start_new_sequence(self):
        if self.game_logic.lives <= 0:
            self.save_score()
            self.update_labels()
            self.show_lost_popup()
        else:
            self.game_logic.increase_difficulty()
            self.update_grid_layout()
            self.update_labels()
            self.game_logic.next_sequence()

    def update_labels(self):
        self.points_label.text = f'Points: {self.game_logic.points}'
        if self.game_logic.lives < 0:
            self.game_logic.lives = 0
        self.lives_label.text = f'Lives: {self.game_logic.lives}'


    def show_lost_popup(self):
        main_menu_screen = self.manager.get_screen('menu')
        player_name = main_menu_screen.player_name_input.text
        if player_name == "" or player_name == " ":
            player_name = 'Unknown'
        self.player_name_label.text = f'Name: {player_name}'
        self.player_score_label.text = f'Score: {self.game_logic.points}'
        self.lost_popup.open()

    def start_game(self, instance=None):
        self.game_logic.reset_game()
        self.update_grid_layout()
        self.update_labels()
        self.game_logic.next_sequence()
        self.lost_popup.dismiss()

    def go_to_menu(self, instance=None):
        self.game_logic.reset_game()
        self.update_grid_layout()
        self.update_labels()
        self.manager.current = 'menu'
        self.lost_popup.dismiss()

    def save_score(self):
        main_menu_screen = self.manager.get_screen('menu')
        player_name = main_menu_screen.player_name_input.text
        score = self.game_logic.points

        if player_name == "" or player_name == " ":
            player_name = 'Unknown'

        self.data_management.save_high_score(score, player_name)

    def on_enter(self):
        self.start_game()
