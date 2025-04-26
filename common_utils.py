"""
Common Utils

Return calendar dates (year, month, week, weekdays)
"""

import calendar
from datetime import datetime

LOCAL_CALENDAR = calendar.LocaleTextCalendar(firstweekday=6)
TODAY = datetime.today()
COLOUR_RGBA_SELECTED: list = [0.4, 0.9, 1, 1]

# ...datescalendar returns MonthList[WeekList[datetime.date]]
def get_month(year: int, month: int) -> list:
    """
    Get datetime by month

    Returns month[week][date]
    """
    month_keys = LOCAL_CALENDAR.monthdatescalendar(year, month)
    return month_keys

def get_month_name(month: int) -> str:
    """
    Returns Month name as a string
    """
    month_index = month
    return calendar.month_name[month_index]

def get_week_number(current_day: datetime) -> str:
    """
    Get current day value -> Return that date's week number
    """
    return current_day.strftime('%U')

def get_week_days(this_day: datetime) -> list:
    """
    Get current day value -> Return datetime values of that day's week as a list

    Checks if current day value is in [week] list (use entire year)
    -> If true, convert those values to string (MM/DD)
    -> Add to week_index list for exporting
    """
    current_day = this_day.date()
    month_list = LOCAL_CALENDAR.monthdatescalendar(this_day.year, this_day.month)
    for week in month_list:
        if current_day in week:
            return [d.strftime('%m/%d') for d in week]
    return []

def get_grid_rows(gridlayout) -> int:
    """ Get id of dynamically populated GridLayout to calculate number of rows """
    children_count: int = len(gridlayout.children)
    cols: int = gridlayout.cols

    if not cols:
        raise ValueError("GridLayout must have 'cols' set to calculate rows dynamically.")

    rows: int = (children_count + cols - 1) // cols
    return rows
