"""
*** UNUSED ATM ***

This file stores animations
"""

from kivy.animation import Animation

def _scrollview_snap(self, layout):
    """
    Used for snapping grids to fixed bars on scrollable views for selection

    Referenced in TimeSelector
    """
    scrollview = self.ids.time_scroll_view
    children = self.ids.time_scroll_view.children

    if not children:
        return

    center_y = scrollview.to_widget(scrollview.center_x, scrollview.center_y)[1] # [0] = x, [1] = y
    closest = min(children, key=lambda w: abs(w.center_y - center_y))
    scroll_target_y = (closest.y + closest.height / 2) - (scrollview.height / 2)
    max_scroll_y = layout.height - scrollview.height
    scroll_target_y = max(0, min(scroll_target_y, max_scroll_y))
    scroll_y = 1 - (scroll_target_y / max_scroll_y) if max_scroll_y > 0 else 1

    if abs(scrollview.scroll_y - scroll_y) < 0.01: # don't snap if close enough
        return

    Animation(scroll_y=scroll_y, d=0.2).start(scrollview)
