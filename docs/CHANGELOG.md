# WIP:

- WeekView functionality
- Event data editing
- Display daily events in MonthView

######

2025/04/11

# ADDED:

- Event sorting by date & time
- View switching (YearView <-> MonthView <-> WeekView)
- YearView & MonthView navigation streamlined (retaining current month/year data)
- Opening MonthView by clicking on month in YearView
- CHANGELOG.md

# CHANGED:

- Event GUI properties (padding, spacing, alignment)
- Separated view logic file & core functions file for clarity
- Navigation logic now checks for booleans instead of strings - hoping for performance boost
- Moved README content over to new CHANGELOG as it's more appropriate here
- Now using ISO

2025/04/10

# FIXED:

- Date selector now displays Sunday as first day of week (used to be Monday) [(weekday + 6) % 7]

2025/04/09

# ADDED:

- 'Add Event' button functionality in AddEventPopup (Save event data to db.json file -> close popup)
- Loading event data to DayView

2025/04/08

# ADDED:

- CalendarUI (Month View)
  - Navigation between months
  - Clickable buttons for each day
- Day View
  - Add Event button
- Add Event Popup
  - Clickable buttons for start/end day & start/end time
  - Day selector - calendar view
    - Calendar navigation complete
    - Pressing on buttons save date for later use -> returns as datetime.date() type
    - Button widget text updates upon selecting & closing selector popup window
  - Time selector - meridiem indicator/hour/minute, scrollable
    - Button Actions complete
    - Pressing on buttons save date for later use -> returns as datetime.time() type
    - Button widget text updates upon selecting & closing selector popup window
