"""
Common Utils

Return calendar dates (year, month, week, weekdays)
"""

import calendar
from datetime import datetime, date

LOCAL_CALENDAR = calendar.LocaleTextCalendar(firstweekday=6)
TODAY = datetime.today()
COLOUR_RGBA_SELECTED: list = [0.4, 0.9, 1, 1]

def current_date(year: int = None, month: int = None, day: int = None) -> date:
    """
    Used to track current date on the screen - returns date object (no time data)

    Parameters received = year, month, date
    """
    td = date.today()
    _year, _month, _day = td.year, td.month, td.day
    if year:
        _year = year
    if month:
        _month = month
    if day:
        _day = day
    new_date = date(_year, _month, _day)
    return new_date

# ...datescalendar returns MonthList[WeekList[datetime.date]]
def get_year(year: int) -> list:
    """
    Get datetime by year

    Returns year[month][0][week][date]
    (width=1 reduces month sets to 1, so use that to get month)
    """
    year_keys = LOCAL_CALENDAR.yeardatescalendar(year, width=1)
    return year_keys

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

def get_week_days(current_day: datetime) -> list:
    """
    Get current day value -> Return datetime values of that day's week

    Checks if current day value is in [week] list (use entire year)
    -> If true, convert those values to string (MM/DD)
    -> Add to week_index list for exporting
    """
    year: int = current_day.year
    current_date = current_day.date()
    year_list = get_year(year)
    week_index = []
    for m in year_list:
        for w in m[0]:
            try:
                if current_date in w:
                    for d in w:
                        d = d.strftime('%m/%d')
                        week_index.append(d)
                        if len(week_index) == 7:
                            return week_index
            except IndexError:
                break
