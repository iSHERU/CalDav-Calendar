from caldav import DAVClient
from caldav.lib import error
from datetime import datetime, timedelta
import traceback
from icalendar import Calendar, Event
from google_calendar import start, end
from google_calendar import summary as sum

# CalDAV server URL and credentials
url = 'your_caldav_url'
username = 'your_user_name'
password = 'your_user_name'

try:
    # Connect to the CalDAV server
    client = DAVClient(url=url, username=username, password=password)
    
    # Get list of calendars
    principal = client.principal()
    calendars = principal.calendars()
    
    # Print list of calendar names
    print("Calendars:")
    for calendar in calendars:
        print(f"- {calendar.name}")
    
    # Example: Fetch events from a specific calendar
    if calendars:
        calendar = calendars[0]  # Choose the first calendar, for example
        
        # Fetch events from the calendar
        events = calendar.events()
        
        # Print event details
        print("\nEvents:")
        if events:
            for event in events:
                cal = Calendar.from_ical(event.data)
                for component in cal.walk():
                    if component.name == "VEVENT":
                        summary = component.get("SUMMARY")
                        print(f"- {summary}")

        else:
            print("No Events Yet.")
        
        # Example: Create a new event
        print("\nCreating new event...")
        
        dt_format = '%Y-%m-%d'
        start_time = datetime.strptime(start, dt_format)  # assuming start is in ISO 8601 format
        end_time = datetime.strptime(end, dt_format)  # assuming end is in ISO 8601 format

        # Create the event
        cal = Calendar()
        event = Event()
        event.add('summary', sum)
        event.add('dtstart', start_time)
        event.add('dtend', end_time)
        cal.add_component(event)

        new_event = calendar.add_event(cal.to_ical().decode('utf-8'))
        
        print("\nEvent created successfully:")

    else:
        print("\nNo calendars found.")

except error.AuthorizationError as e:
    print("Authorization error:", e)
    traceback.print_exc()
    
except ValueError as e:
    print("Value error occurred", e)
    traceback.print_exc()
    
except Exception as e:
    print("An error occurred:", e)
    traceback.print_exc()
