README

25/04/08

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

25/04/09

- 'Add Event' button functionality in AddEventPopup
  - Save event data to db.json file -> close popup
  - Event data loaded to DayView

25/04/10
- Fixed date selector to display Sunday as first day of week (weekday + 6) % 7

25/04/11
- Events sorted by date & time
- Adjusted event GUI properties (padding, spacing, alignment)
- Started coding year_view (need to add logic to switch view)