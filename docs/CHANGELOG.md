## TODO:

- Important! factor will display on YearView specifically (I haven't yet decided the details on how to implement)

- Change time selector graphic display to show selected values in the center
- Display additional event data (other than time, date, title) as icons (with mouse hover tooltip?) in DayView
- Event editing
- Settings tab
- 'Today' button to move back to current day's MonthView instantly
- Display daily events in MonthView
- Fix WeekView (looks lame atm)
- Animations
- Change Event colours to match group tag colour

## ISSUES:

- YearView Grid - current system is very slow - takes too long to calculate entire month grid for each month

---

## 2025/05/02

- CHANGED: Date selector UI

---

## 2025/05/01

- CHANGED: AddEvent popup UI
- CHANGED: Colour selector UI
- ADDED: AppleSDGothicNeo font -> set to default (normal, bold)
- ADDED: NanumSquareRound package (not applied)
- CHANGED: Locale settings to korean -> started localization of app to korean
- ADDED: Function to get korean year-month format (for use in titles)

---

## 2025/04/30

- ADDED: MonthGrid: selected grid highlighting
- CHANGED: DayView from Popup -> BoxLayout widget (for better UI customization)
- CHANGED: DayView UI & Event colours
- FIXED: YearView now looks for CoreFunctions to switch view, instead of a pre-defined parent chain (which caused crashes)
- Divided views.kv -> main_views.kv, day_view.kv, event_popups.kv for readability

---

## 2025/04/28

- CHANGED: YearView UI
- ADDED: MonthView Grid UI
- ADDED: Loading MonthView from YearView
- FIX: Date synchronization between views

---

## 2025/04/27

- ADDED: Grid lines for MonthView
- ADDED: Text colour for Sunday is RED now

---

## 2025/04/25

- ADDED: New box layout to template for month grid blocks
- UI Update for MonthView

---

## 2025/04/25

- ADDED: UI Palette file
- Canvas, UI update

---

## 2025/04/18

- ADDED: TODAY constant
- FIX: Navigation direction for YearView & WeekView
- Optimizations for WeekView generation

---

## 2025/04/17

- ADDED: COLOUR_RGBA_SELECTED global variable now controls colours displayed for selected values
- Colour Picker: "Selected Colour" text previews the selected colour in real-time
- Commented out code related to time selector's fixed bar. Visual & behaviour coding will continue later
- Time Selector: Added OK / Cancel buttons to make saving / cancelling time selection more straightforward
  - Closing Time selector in any method other than clicking OK will result in just closing the popup without saving
- Time Selector: Now displays currently selected time correctly when opened
- Window size adjusted to iPhone 13 (half-scale) resolution

---

## 2025/04/15

- ADDED: Group tags, Repeat, Repeat details, Notification, Notification details and Important? attributes to event
  - Group tag naming
  - Basic 2x3 colour selector for selecting group tag colours
  - Repeat checkbox
  - Notification checkbox
  - Important? checkbox
- ADDED: requirements.txt (currently only contains Kivy 2.3.1)
- Changes applied to ViewEvent Popup as well
- Date selector: clicking on a selected date will now close the selector and store the selected day value
- Time selector: added fixed bar to use as a time selector - WIP

---

## 2025/04/14

- ViewEvent Popup
- Loaded events in DayView are now BoxLayouts with ButtonBehaviour
- Added new KV class DayViewEvent to use as template for loaded events
- DayView refreshes immediately after adding new event
- Moved the Event Layout Widget from python script to view.kv for reusability
- Edited README to show current roadmap phases correctly
- FIX: Wrong direction (left/right, up/down) caused by inverted swiping vs arrow keys now works correctly

---

## 2025/04/13

- ADDED: WeekView displays events of the day (title only)
- ADDED: 'key' Key to events data - will be used to call up events ('key' will start from 1)
- CHANGED: Days of week displays Sunday to Saturday correctly
- REMOVED: WeekGrid canvas widget

---

## 2025/04/12

- ADDED: WeekView display
- ADDED: WeekView navigation (previous/next week)
- ADDED: Explanation dialog for Database class

---

## 2025/04/11

- ADDED: Event sorting by date & time
- ADDED: View switching (YearView <-> MonthView <-> WeekView)
- ADDED: YearView & MonthView navigation streamlined (retaining current month/year data)
- ADDED: Opening MonthView by clicking on month in YearView
- ADDED: CHANGELOG.md
- CHANGED: Event GUI properties (padding, spacing, alignment)
- CHANGED: Separated view logic file & core functions file for clarity
- CHANGED: Navigation logic now checks for booleans instead of strings - hoping for performance boost
- CHANGED: Moved README content over to new CHANGELOG as it's more appropriate here
- CHANGED: Now using ISO

---

## 2025/04/10

- FIX: Date selector now displays Sunday as first day of week (used to be Monday) [(weekday + 6) % 7]

---

## 2025/04/09

- ADDED: 'Add Event' button functionality in AddEventPopup (Save event data to db.json file -> close popup)
- ADDED: Loading event data to DayView

---

## 2025/04/08

- ADDED: CalendarUI (Month View)
  - Navigation between months
  - Clickable buttons for each day
- ADDED: Day View
  - Add Event button
- ADDED: Add Event Popup
  - Clickable buttons for start/end day & start/end time
  - Day selector - calendar view
    - Calendar navigation complete
    - Pressing on buttons save date for later use -> returns as datetime.date() type
    - Button widget text updates upon selecting & closing selector popup window
  - Time selector - meridiem indicator/hour/minute, scrollable
    - Button Actions complete
    - Pressing on buttons save date for later use -> returns as datetime.time() type
    - Button widget text updates upon selecting & closing selector popup window
