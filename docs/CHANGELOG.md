# TODO:

- Refine selectors <<< HALTED - will continue later >>>

- Important! factor will display on YearView specifically (I haven't yet decided the details on how to implement)

- Change time selector graphic display to show selected values in the center
- Display additional event data (other than time, date, title) as icons (with mouse hover tooltip?) in DayView
- Event editing
- Settings tab
- 'Today' button to move back to current day's MonthView instantly
- Display daily events in MonthView
- Fix WeekView (looks lame atm)
- Korean support, fonts
- Colors, Graphics
- Animations

# ISSUES:

- WeekView synchronization with MonthView and YearView is broken again
- MonthView Grid - gray line is being shown even for empty grids
- MnothView - there's a white box at the bottom left corner
- YearView Grid - current system is very slow - takes too long to calculate entire month grid for each month

---

# 2025/04/28

# \_CHANGED:

- YearView UI
- MonthView Grid UI
- Loading MonthView from YearView

---

# 2025/04/27

# \_ADDED:

- Grid lines for MonthView
- Text colour for Sunday is RED now

---

# 2025/04/25

# \_CHANGED:

- New box layout to template for month grid blocks

# \_ADDED:

- UI Update for MonthView

---

# 2025/04/25

# \_ADDED:

- UI Palette file
- Canvas, UI update

# 2025/04/18

# \_ADDED:

- TODAY constant

# \_FIXED:

- Navigation direction for YearView & WeekView

# CHANGED:

- Optimizations for WeekView generation

---

# 2025/04/17

# \_ADDED:

- COLOUR_RGBA_SELECTED global variable now controls colours displayed for selected values
- Colour Picker: "Selected Colour" text previews the selected colour in real-time

# \_CHANGED:

- Commented out code related to time selector's fixed bar. Visual & behaviour coding will continue later
- Time Selector: Added OK / Cancel buttons to make saving / cancelling time selection more straightforward
  - Closing Time selector in any method other than clicking OK will result in just closing the popup without saving
- Time Selector: Now displays currently selected time correctly when opened
- Window size adjusted to iPhone 13 (half-scale) resolution

---

# 2025/04/15

# \_ADDED:

- Group tags, Repeat, Repeat details, Notification, Notification details and Important? attributes to event
  - Group tag naming
  - Basic 2x3 colour selector for selecting group tag colours
  - Repeat checkbox
  - Notification checkbox
  - Important? checkbox
- Changes applied to ViewEvent Popup as well
- requirements.txt (currently only contains Kivy 2.3.1)

# \_CHANGED:

- Date selector: clicking on a selected date will now close the selector and store the selected day value
- Time selector: added fixed bar to use as a time selector - WIP

---

# 2025/04/14

# \_ADDED:

- ViewEvent Popup
- Loaded events in DayView are now BoxLayouts with ButtonBehaviour
- Added new KV class DayViewEvent to use as template for loaded events
- DayView refreshes immediately after adding new event

# \_CHANGED:

- Moved the Event Layout Widget from python script to view.kv for reusability
- Edited README to show current roadmap phases correctly

# \_FIXED:

- Wrong direction (left/right, up/down) caused by inverted swiping vs arrow keys now works correctly

---

# 2025/04/13

# \_ADDED:

- WeekView displays events of the day (title only)
- 'key' Key to events data - will be used to call up events ('key' will start from 1)

# \_CHANGED:

- Days of week displays Sunday to Saturday correctly

# \_REMOVED:

- WeekGrid canvas widget

---

# 2025/04/12

# \_ADDED:

- WeekView display
- WeekView navigation (previous/next week)
- Explanation dialog for Database class

---

# 2025/04/11

# \_ADDED:

- Event sorting by date & time
- View switching (YearView <-> MonthView <-> WeekView)
- YearView & MonthView navigation streamlined (retaining current month/year data)
- Opening MonthView by clicking on month in YearView
- CHANGELOG.md

# \_CHANGED:

- Event GUI properties (padding, spacing, alignment)
- Separated view logic file & core functions file for clarity
- Navigation logic now checks for booleans instead of strings - hoping for performance boost
- Moved README content over to new CHANGELOG as it's more appropriate here
- Now using ISO

---

# 2025/04/10

# \_FIXED:

- Date selector now displays Sunday as first day of week (used to be Monday) [(weekday + 6) % 7]

---

# 2025/04/09

# \_ADDED:

- 'Add Event' button functionality in AddEventPopup (Save event data to db.json file -> close popup)
- Loading event data to DayView

---

# 2025/04/08

# \_ADDED:

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
