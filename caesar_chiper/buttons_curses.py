"""Module for add button into curses screen."""
import curses

class Button:
    """Button."""

    def __init__(self, name, function, selected=False):
        """Init name, func for callback and selected."""
        self.name = name
        self.action = function
        self.selected = selected

    def toggle(self):
        """Toggle button."""
        self.selected = not self.selected

    def execute(self):
        """Execute callback function."""
        self.action()


class GroupButton:
    """Group of buttons."""

    def __init__(self, stdscr, name, function):
        """Init curses screen and first button."""
        self.stdscr = stdscr
        self.buttons = [Button(name, function, True)]
        self.selected = 0

    def render(self, line, column):
        """Render group of buttons."""
        for button in self.buttons:
            attr = curses.A_REVERSE if button.selected else curses.A_BOLD
            self.stdscr.addstr(line, column, button.name, attr )
            column += 1 + len(button.name)

    def add(self, name, function):
        """Add button in group."""
        self.buttons.append(Button(name, function))

    def next(self):
        """Select next button."""
        self.buttons[self.selected].toggle()
        self.selected = (
            self.selected+1 if self.selected < len(self.buttons)-1 else 0)
        self.buttons[self.selected].toggle()

    def back(self):
        """Select preview button."""
        self.buttons[self.selected].toggle()
        self.selected = (
            self.selected-1 if self.selected > 0 else len(self.buttons)-1)
        self.buttons[self.selected].toggle()

    def push(self):
        """Push on button."""
        self.buttons[self.selected].execute()
