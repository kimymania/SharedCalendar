"""
This is the colour palette

check for dark_theme for theme switching
"""

WHITE = [1, 1, 1, 1]
BLACK = [0, 0, 0, 1]
LIGHT_BLUE = [0.6, 0.85, 0.9, 1]
SELECTED = [0.3, 0.9, 0.5, 0.7]
GRAY = [0.3, 0.3, 0.3, 1]
RED = [1, 0, 0, 1]
GREEN = [0, 1, 0, 1]

dark_theme: bool = False

if not dark_theme:
    background_colour = WHITE
    text_colour = BLACK
    line_colour = LIGHT_BLUE
    selected_colour = SELECTED
    disabled_colour = GRAY
else:
    background_colour = BLACK
    text_colour = WHITE
    line_colour = LIGHT_BLUE
    selected_colour = SELECTED
    disabled_colour = GRAY
