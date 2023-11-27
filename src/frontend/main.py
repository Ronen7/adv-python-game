from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
import sys
sys.path.append('/Path/to/adv-python-game-main/src/frontend')
from screens.game_screen import GameScreen
from screens.menu_screen import MainMenuScreen


class MemoryGameApp(App):
    def build(self):
        Window.size = (360, 640)
        sm = ScreenManager()
        sm.add_widget(MainMenuScreen(name='menu'))
        sm.add_widget(GameScreen(name='game'))
        Window.clearcolor = (1, 1, 1, 1)
        return sm


if __name__ == '__main__':
    MemoryGameApp().run()
