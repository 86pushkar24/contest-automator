from datetime import datetime, timedelta, time, date
from dateutil import tz
from ics import Calendar, Event

ALARM_BLOCK = (
    "BEGIN:VALARM\n"
    "TRIGGER:-PT10M\n"
    "ACTION:DISPLAY\n"
    "DESCRIPTION:Reminder\n"
    "END:VALARM"
)

WEEKLY_DURATION = timedelta(minutes=90)
BIWEEKLY_DURATION = timedelta(minutes=90)
BIWEEKLY_ANCHOR = date(2024, 10, 11)

def prompt_end_date(today):
    while True:
        raw_input = input("Enter the end date for LeetCode contests (YYYY-MM-DD): ").strip()
        try:
            end_date = datetime.strptime(raw_input, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            continue

        if end_date <= today:
            print("End date must be after today's date.")
            continue

        return end_date

def next_weekday(after_date, weekday):
    days_ahead = (weekday - after_date.weekday()) % 7
    if days_ahead == 0:
        days_ahead = 7
    return after_date + timedelta(days=days_ahead)

def next_biweekly_start(today):
    current = BIWEEKLY_ANCHOR
    while current <= today:
        current += timedelta(days=14)
    return current

def add_weekly_contests(calendar, first_date, end_date, timezone):
    current = first_date
    while current <= end_date:
        start_dt = datetime.combine(current, time(8, 0), tzinfo=timezone)
        event = Event(
            name="LeetCode Weekly Contest",
            begin=start_dt,
            end=start_dt + WEEKLY_DURATION,
            description="LeetCode Weekly Contest."
        )
        calendar.events.add(event)
        current += timedelta(days=7)

def add_biweekly_contests(calendar, first_date, end_date, timezone):
    current = first_date
    while current <= end_date:
        start_dt = datetime.combine(current, time(20, 0), tzinfo=timezone)
        if start_dt.weekday() != 5:
            offset = (5 - start_dt.weekday()) % 7
            start_dt += timedelta(days=offset)
            current = start_dt.date()
        event = Event(
            name="LeetCode Biweekly Contest",
            begin=start_dt,
            end=start_dt + BIWEEKLY_DURATION,
            description="LeetCode Biweekly Contest."
        )
        calendar.events.add(event)
        current += timedelta(days=14)

def inject_alarms(ics_text):
    return ics_text.replace("END:VEVENT", f"{ALARM_BLOCK}\nEND:VEVENT")

def main():
    timezone = tz.gettz("Asia/Kolkata")
    if timezone is None:
        raise RuntimeError("Unable to load Asia/Kolkata timezone data.")

    today = datetime.now(timezone).date()
    end_date = prompt_end_date(today)
    first_weekly = next_weekday(today, 6)
    first_biweekly = next_biweekly_start(today)

    calendar = Calendar()

    if first_weekly <= end_date:
        add_weekly_contests(calendar, first_weekly, end_date, timezone)

    if first_biweekly <= end_date:
        add_biweekly_contests(calendar, first_biweekly, end_date, timezone)

    if not calendar.events:
        print("No LeetCode contests fall within the provided range.")
        return

    ics_text = inject_alarms(str(calendar))
    output_file = "leetcode_contests.ics"

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(ics_text)

    print("Created leetcode_contests.ics with upcoming weekly and biweekly contests.")
    print("Each event includes a reminder 10 minutes before the start time.")
    print("Biweekly contests assume the next occurrence on 11 October 2024 and repeat every 14 days.")

if __name__ == "__main__":
    main()
