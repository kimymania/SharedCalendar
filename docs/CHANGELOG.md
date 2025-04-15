# TODO:

- Need to implement live updates for color picker
- Important! factor will display on YearView specifically (I haven't yet decided the details on how to implement)

- I think changes to event data should be made first, to avoid re-writing as much as possible

- Change date & time selectors' popup close & save method - currently, user has to click/press any other place on the screen
- Change time selector graphic display to show selected values in the center
- Display additional event data (other than time, date, title) as icons (with mouse hover tooltip?) in DayView
- Event editing
- Settings tab
- 'Today' button to move back to current day's MonthView instantly
- Display daily events in MonthView
- Display month & dates properly in YearView (Button -> BoxLayout w/ ButtonBehavior?)
- Fix WeekView (looks lame atm)
- Korean support
- Dependencies file (kivy fonts)
- Colors, Graphics
- Animations

######

2025/04/15

# ADDED:
- Group tags, Repeat, Repeat details, Notification, Notification details and Important? factors to event
  - Group tag naming
  - Basic 2x3 colour selector for selecting group tag colours 
  - Repeat checkbox
  - Notification checkbox
  - Important? checkbox
- requirements.txt (currently only contains Kivy 2.3.1)

2025/04/14

# ADDED:
- ViewEvent Popup
- Loaded events in DayView are now BoxLayouts with ButtonBehaviour
- Added new KV class DayViewEvent to use as template for loaded events
- DayView refreshes immediately after adding new event

# CHANGED:
- Moved the Event Layout Widget from python script to view.kv for reusability
- Edited README to show current roadmap phases correctly

# FIXED:
- Wrong direction (left/right, up/down) caused by inverted swiping vs arrow keys now works correctly

2025/04/13

# ADDED:
- WeekView displays events of the day (title only)
- 'key' Key to events data - will be used to call up events ('key' will start from 1)

# CHANGED:
- Days of week displays Sunday to Saturday correctly

# REMOVED:
- WeekGrid canvas widget

2025/04/12

# ADDED:
- WeekView display
- WeekView navigation (previous/next week)
- Explanation dialog for Database class

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
