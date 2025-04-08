import calendar

LOCAL_CALENDAR = calendar.LocaleTextCalendar(firstweekday=6)

# ...datescalendar returns MonthList[WeekList[datetime.date]]
def get_year(year: int) -> list:
    """ get datetime by year """
    year_keys = LOCAL_CALENDAR.yeardatescalendar(year)
    return year_keys

def get_month(year: int, month: int) -> list:
    """ get datetime by month """
    month_keys = LOCAL_CALENDAR.monthdatescalendar(year, month)
    return month_keys

def get_week(year: int, month: int, day: int) -> str:
    """ get day numbers by week """
    month_calendar = get_month(year, month)

    # Find the week containing the specified day
    for week in month_calendar:
        if day in week:
            return ' '.join(str(d) if d != 0 else ' ' for d in week)

    # Day not found in the month
    return "Invalid date"
