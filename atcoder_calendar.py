from datetime import datetime, timedelta, time
from dateutil import tz
from ics import Calendar, Event

ALARM_BLOCK = (
    "BEGIN:VALARM\n"
    "TRIGGER:-PT10M\n"
    "ACTION:DISPLAY\n"
    "DESCRIPTION:Reminder\n"
    "END:VALARM"
)

def prompt_end_date(today):
    while True:
        raw_input = input("Enter the end date for AtCoder contests (YYYY-MM-DD): ").strip()
        try:
            end_date = datetime.strptime(raw_input, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            continue

        if end_date <= today:
            print("End date must be after today's date.")
            continue

        return end_date

def next_saturday(after_date):
    days_ahead = (5 - after_date.weekday()) % 7
    if days_ahead == 0:
        days_ahead = 7
    return after_date + timedelta(days=days_ahead)

def build_events(start_date, end_date, timezone):
    calendar = Calendar()
    current_date = start_date

    while current_date <= end_date:
        start_dt = datetime.combine(current_date, time(17, 30), tzinfo=timezone)
        end_dt = start_dt + timedelta(minutes=100)

        event = Event(
            name="AtCoder Beginner Contest",
            begin=start_dt,
            end=end_dt,
            description="Weekly AtCoder Beginner Contest."
        )

        calendar.events.add(event)
        current_date += timedelta(days=7)

    return calendar

def inject_alarms(ics_text):
    return ics_text.replace("END:VEVENT", f"{ALARM_BLOCK}\nEND:VEVENT")

def main():
    timezone = tz.gettz("Asia/Kolkata")
    if timezone is None:
        raise RuntimeError("Unable to load Asia/Kolkata timezone data.")

    today = datetime.now(timezone).date()
    end_date = prompt_end_date(today)
    first_contest_date = next_saturday(today)

    if first_contest_date > end_date:
        print("No contests fall within the provided range.")
        return

    calendar = build_events(first_contest_date, end_date, timezone)
    ics_text = inject_alarms(str(calendar))
    output_file = "atcoder_beginner_contest.ics"

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(ics_text)

    print(f"Created {output_file} with AtCoder Beginner Contests from {first_contest_date} to {end_date}.")
    print("Each event includes a reminder 10 minutes before the contest starts.")
    print("Duration is set to 100 minutes (standard ABC length). Adjust the script if that changes.")

if __name__ == "__main__":
    main()
