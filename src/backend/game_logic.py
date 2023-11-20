import random  # For generating random numbers
import time  # For handling time in the game
from kivy.app import App  # For managing the Kivy application
from kivy.uix.gridlayout import GridLayout  # For creating the grid layout of buttons
from kivy.uix.button import Button  # For creating buttons
from kivy.clock import Clock  # For controlling time and timers in Kivy
from kivy.event import EventDispatcher  # For event handling in Kivy


class GameLogic:
    def _init_(self):
        self.num = 3  # Number of buttons that will change color
        self.cols = 4  # Grid size - columns
        self.lines = 4  # Grid size - rows
        self.num_buttons = self.cols * self.lines  # Total number of buttons
        self.sequence = []  # Sequence of colored buttons
        self.current_sequence = []  # User-selected sequence of buttons
        self.colors = [(1, 0, 1, 1), (1, 1, 1, 1), (1, 0, 0, 1)]  # Colors: purple, white, red
        self.time_limit = 4.0  # Time limit to display colored buttons
        self.turn = 0  # Counter for the game turns
        self.life=3 #counter for life points

    def start_game(self):
        # Step 1: Generate a new sequence of colored buttons
        self.generate_sequence()
        # Step 2: Display the generated sequence
        self.display_sequence()

    def generate_sequence(self):

        # Step 1: Reset the color of the buttons
        self.reset_colors()

        # HERE GOES THE CREATION OF THE GRID, ATTENTION TO THE INCREASE DIFFICULTY THAT MAY INCREMENT COLS AND LINES

        # Generate 'num' random indices for the sequence
        self.sequence = random.choices(range(self.num_buttons), k=self.num)

    def display_sequence(self):
        # Step 1: Display the sequence of colored buttons
        for button_index in self.sequence:
            # Color the buttons in the sequence purple
            button = self.buttons[button_index]
            button.background_color = (1, 0, 1, 1)
        # Step 2: Set a timer to reset the colors after 'time_limit' seconds
        Clock.schedule_once(self.reset_colors, self.time_limit)

    def on_button_click(self, instance):
        if instance in self.buttons:  # Checks if the clicked instance is a valid button
            if instance.background_color != (1, 0, 1, 1):
                # Checks if the button is not already purple
                self.current_sequence.append(
                    self.buttons.index(instance))  # Adds the button index to the current sequence

                if self.buttons.index(instance) in self.sequence:
                    # If the button index is in the correct sequence, colors the button purple
                    instance.background_color = (1, 0, 1, 1)
                    self.dispatch('on_button_colored',instance)  # Dispatch an event 'on_button_colored' (a front end function) to notify the front-end that a button has been colored with the given instance.
                else:
                    # If the button index is not in the correct sequence, colors the button red
                    instance.background_color = (1, 0, 0, 1)
                    self.dispatch('on_button_colored',instance)  # # Dispatch an event 'on_button_colored' (a front end function) to notify the front-end that a button has been colored with the given instance.
                    time.sleep(1)  # Pauses execution for 1 second
                    instance.background_color = (1, 1, 1, 1)
                    self.dispatch('on_button_colored',instance)
                    self.life -=1
                if self.life == 0 :
                    self.display_end_game()  # Displays the end game screen

                if len(self.current_sequence) == self.num:
                    # If the current sequence length matches the number of buttons in the sequence
                    self.increase_difficulty()  # Increases the game difficulty

    def increase_difficulty(self):
        # Step 1: Randomly choose an option to increase difficulty: buttons, time, or grid
        choice = random.choice(["buttons", "time", "grid"])
        if choice == "buttons":
            # Step 2: Increase the number of buttons in the sequence if it's less than half the total buttons
            if self.num < len(self.num_buttons) / 2:
                self.num += 1
        elif choice == "time":
            # Step 3: Decrease the time limit for displaying colored buttons
            self.time_limit -= 0.5
            if self.time_limit < 1.0:  # Limit the minimum time limit
                self.time_limit = 1.0
        elif choice == "grid":
            # Step 4: Increase either the columns or rows in the grid
            if self.cols > self.lines:  # to make colums or row very similiar
                self.lines += 1
            else:
                self.cols += 1
        self.turn +=1
        self.generate_sequence()

    def display_end_game(self):
        # To be implemented: Display the end game window that gives two choices: restart (go to self.start) or go to the menu
        pass

    def reset_colors(self, dt):
        # Reset the colors of all buttons to white after the time limit
        for button in self.buttons:
            button.background_color = (1, 1, 1, 1)