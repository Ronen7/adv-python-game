import random
from kivy.clock import Clock


class GameLogic:
    def __init__(self):
        self.num = 3
        self.cols = 3
        self.sequence = []
        self.sequence_check = []
        self.lives = 3
        self.points = 0
        self.buttons = []
        self.sequence_index = 0
        self.rounds = 0
        self.scheduled_event = None
        self.display_delay = 2

    def set_buttons(self, buttons):
        self.buttons = buttons

    def start_game(self):
        self.generate_sequence()
        self.display_sequence()

    def reset_game(self):
        self.sequence = []
        self.sequence_index = 0
        self.lives = 3
        self.num = 3
        self.cols = 3
        self.rounds = 0
        self.points = 0
        if self.scheduled_event is not None:
            Clock.unschedule(self.scheduled_event)

    def generate_sequence(self):
        self.sequence = random.sample(range(self.cols * self.cols), self.num)
        self.sequence_check = list(self.sequence)

    def display_sequence(self):
        for index in self.sequence:
            self.buttons[index].background_color = (1, 0, 1, 1)
        self.scheduled_event = Clock.schedule_once(lambda dt: self.hide_sequence(), self.display_delay)

    def hide_sequence(self):
        for index in self.sequence:
            self.buttons[index].background_color = (1, 1, 1, 1)

    def check_tile(self, tile_index):
        if tile_index in self.sequence and tile_index in self.sequence_check:
            self.sequence_index += 1
            self.sequence.remove(tile_index)
            return {'status': 'correct', 'tile_index': tile_index}
        elif tile_index in self.sequence_check:
            self.sequence_index -= 1
            self.sequence.append(tile_index)
            return {'status': 'double_click', 'tile_index': tile_index}
        else:
            self.lives -= 1
            self.rounds += 1
            return {'status': 'wrong'}

    def check_sequence(self):
        if self.sequence_index == self.num:
            self.rounds += 1
            self.points += 1
            return {'status': 'correct'}
        else:
            return {'status': 'wrong'}

    def next_sequence(self):
        self.generate_sequence()
        self.display_sequence()
        self.sequence_index = 0

    def increase_difficulty(self):
        if self.rounds % 7 == 0:
            self.num -= 1
        elif self.rounds % 4 == 0:
            self.num += 1
            self.cols += 1
        elif self.rounds % 2 == 0:
            self.num += 1

        self.display_delay = max(self.display_delay - 0.05, 1)
