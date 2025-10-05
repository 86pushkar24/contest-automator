from datetime import datetime, timedelta, time
from dateutil import tz
from ics import Calendar, Event


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


def prompt_reminder_minutes(default=10):
    while True:
        raw_input = input(
            "Reminder lead time in minutes before each contest (press Enter for 10): "
        ).strip()

        if not raw_input:
            return default

        try:
            minutes = int(raw_input)
        except ValueError:
            print("Please enter a whole number of minutes.")
            continue

        if minutes < 0:
            print("Reminder lead time cannot be negative.")
            continue

        return minutes


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


def inject_alarms(ics_text, reminder_minutes):
    alarm_block = (
        "BEGIN:VALARM\n"
        f"TRIGGER:-PT{reminder_minutes}M\n"
        "ACTION:DISPLAY\n"
        "DESCRIPTION:Reminder\n"
        "END:VALARM"
    )
    return ics_text.replace("END:VEVENT", f"{alarm_block}\nEND:VEVENT")


def main():
    timezone = tz.gettz("Asia/Kolkata")
    if timezone is None:
        raise RuntimeError("Unable to load Asia/Kolkata timezone data.")

    today = datetime.now(timezone).date()
    end_date = prompt_end_date(today)
    reminder_minutes = prompt_reminder_minutes()
    first_contest_date = next_saturday(today)

    if first_contest_date > end_date:
        print("No contests fall within the provided range.")
        return

    calendar = build_events(first_contest_date, end_date, timezone)
    ics_text = inject_alarms(str(calendar), reminder_minutes)
    output_file = "atcoder_beginner_contest.ics"

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(ics_text)

    print(
        f"Created {output_file} with AtCoder Beginner Contests from {first_contest_date} to {end_date}."
    )
    print(
        f"Each event includes a reminder {reminder_minutes} minute(s) before the contest starts."
    )
    print("Duration is set to 100 minutes (standard ABC length). Adjust the script if that changes.")


if __name__ == "__main__":
    main()
