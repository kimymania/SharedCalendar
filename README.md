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
  - WIP: Load event data to DayView
    - Events are not loaded in order of start time
    - Align text to the left
