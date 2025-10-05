"""Interactive contest calendar generator for multiple competitive programming platforms."""

from __future__ import annotations

from datetime import date, datetime, time, timedelta
from typing import Callable, Dict, List, Optional, Tuple

import requests
from dateutil import tz
from dateutil.relativedelta import relativedelta
from ics import Calendar, Event


PlatformHandler = Callable[[int, Calendar], bool]


def prompt_menu_choices(options: Dict[str, str]) -> List[str]:
    """Prompt the user to pick one or more keys from the provided options."""
    keys = list(options.keys())
    while True:
        print("Select contest platforms:")
        for index, key in enumerate(keys, start=1):
            print(f"  {index}. {options[key]}")
        print("  0. All platforms")

        raw_choice = input(
            "Enter option numbers separated by commas (e.g. 1,3) or 0 for all: "
        ).strip()
        if not raw_choice:
            print("Please choose at least one option.")
            continue

        choices = [part.strip() for part in raw_choice.replace(",", " ").split() if part.strip()]
        if not choices:
            print("Please choose at least one option.")
            continue

        if any(choice.lower() in {"0", "all", "a"} for choice in choices):
            return keys

        selected: List[str] = []
        invalid_selection = False
        for choice in choices:
            try:
                numeric_choice = int(choice)
            except ValueError:
                invalid_selection = True
                break
            if not 1 <= numeric_choice <= len(keys):
                invalid_selection = True
                break
            key = keys[numeric_choice - 1]
            if key not in selected:
                selected.append(key)

        if invalid_selection or not selected:
            print("Choice out of range. Try again.")
            continue

        return selected


def prompt_non_negative_int(prompt: str, default: Optional[int] = None) -> int:
    """Prompt for a non-negative integer, accepting an optional default."""
    while True:
        raw_input_value = input(prompt).strip()
        if not raw_input_value and default is not None:
            return default
        try:
            value = int(raw_input_value)
        except ValueError:
            print("Please enter a whole number.")
            continue
        if value < 0:
            print("Please enter zero or a positive number.")
            continue
        return value


def inject_alarms(ics_text: str, reminder_minutes: int) -> str:
    alarm_block = (
        "BEGIN:VALARM\n"
        f"TRIGGER:-PT{reminder_minutes}M\n"
        "ACTION:DISPLAY\n"
        "DESCRIPTION:Contest reminder\n"
        "END:VALARM"
    )
    return ics_text.replace("END:VEVENT", f"{alarm_block}\nEND:VEVENT")


def fetch_codeforces_contests(limit: Optional[int] = None) -> list:
    api_url = "https://codeforces.com/api/contest.list"
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        raise RuntimeError(f"Failed to contact Codeforces API: {exc}") from exc

    if payload.get("status") != "OK":
        raise RuntimeError("Unexpected response from Codeforces API.")

    contests = payload.get("result", [])
    upcoming_cf = [
        contest
        for contest in contests
        if contest.get("phase") == "BEFORE"
        and contest.get("type") == "CF"
        and "startTimeSeconds" in contest
    ]
    if limit is None:
        return upcoming_cf
    return upcoming_cf[:limit]


def handle_codeforces(reminder_minutes: int, calendar: Calendar) -> bool:
    try:
        contests = fetch_codeforces_contests()
    except RuntimeError as error:
        print(error)
        return False

    if not contests:
        print("No upcoming Codeforces contests were found.")
        return False

    local_timezone = tz.tzlocal()
    events_added = False

    grouped: Dict[int, List[dict]] = {}
    for contest in contests:
        start_ts = contest.get("startTimeSeconds")
        if start_ts is None:
            continue
        grouped.setdefault(start_ts, []).append(contest)

    def choose_primary(entries: List[dict]) -> dict:
        preferred_order = ["Div. 2", "Div. 3", "Div. 4", "Div. 1"]
        for keyword in preferred_order:
            for entry in entries:
                if keyword in entry.get("name", ""):
                    return entry
        return entries[0]

    for start_ts, grouped_contests in sorted(grouped.items()):
        primary = choose_primary(grouped_contests)
        start_utc = datetime.fromtimestamp(start_ts, tz=tz.tzutc())
        start_local = start_utc.astimezone(local_timezone)
        duration_seconds = primary.get("durationSeconds", 0)
        duration = timedelta(seconds=duration_seconds)

        event = Event()
        event.name = primary.get("name", "Codeforces Contest")
        event.begin = start_local
        event.duration = duration
        event.url = f"https://codeforces.com/contest/{primary.get('id')}"

        description_lines = [
            f"Type: {primary.get('kind', 'Codeforces Round')}",
            f"Duration: {duration}",
        ]

        if difficulty := primary.get("difficulty"):
            description_lines.append(f"Difficulty: {difficulty}")
        if city := primary.get("city"):
            description_lines.append(f"City: {city}")
        if country := primary.get("country"):
            description_lines.append(f"Country: {country}")
        if icpc_region := primary.get("icpcRegion"):
            description_lines.append(f"ICPC Region: {icpc_region}")

        others = [c for c in grouped_contests if c is not primary]
        if others:
            description_lines.append("Other divisions at the same time:")
            for entry in others:
                description_lines.append(f"- {entry.get('name', 'Unnamed contest')}")

        event.description = "\n".join(description_lines)
        calendar.events.add(event)
        events_added = True

    if not events_added:
        print("No Codeforces events to add to the calendar.")
        return False

    return True


def next_weekday(after_date: date, weekday: int) -> date:
    days_ahead = (weekday - after_date.weekday()) % 7
    if days_ahead == 0:
        days_ahead = 7
    return after_date + timedelta(days=days_ahead)


def generate_weekly_events(
    calendar: Calendar,
    first_date: date,
    end_date: date,
    timezone,
    start_time: time,
    duration: timedelta,
    name: str,
    description: str,
) -> None:
    current_date = first_date
    while current_date <= end_date:
        start_dt = datetime.combine(current_date, start_time, tzinfo=timezone)
        event = Event(
            name=name,
            begin=start_dt,
            end=start_dt + duration,
            description=description,
        )
        calendar.events.add(event)
        current_date += timedelta(days=7)


def handle_codechef(reminder_minutes: int, calendar: Calendar) -> bool:
    timezone = tz.gettz("Asia/Kolkata")
    if timezone is None:
        print("Unable to load Asia/Kolkata timezone data.")
        return False

    today = datetime.now(timezone).date()
    end_date = today + relativedelta(months=+6)
    first_contest = next_weekday(today, 2)  # Wednesday
    if first_contest > end_date:
        print("No contests fall within the provided range.")
        return False

    before_count = len(calendar.events)
    generate_weekly_events(
        calendar,
        first_contest,
        end_date,
        timezone,
        time(20, 0),
        timedelta(hours=2),
        "CodeChef Weekly Contest",
        "CodeChef weekly contest.",
    )

    if len(calendar.events) == before_count:
        print("No CodeChef contests were added to the calendar.")
        return False

    return True


def handle_atcoder(reminder_minutes: int, calendar: Calendar) -> bool:
    timezone = tz.gettz("Asia/Kolkata")
    if timezone is None:
        print("Unable to load Asia/Kolkata timezone data.")
        return False

    today = datetime.now(timezone).date()
    end_date = today + relativedelta(months=+6)
    first_contest = next_weekday(today, 5)  # Saturday
    if first_contest > end_date:
        print("No contests fall within the provided range.")
        return False

    before_count = len(calendar.events)
    generate_weekly_events(
        calendar,
        first_contest,
        end_date,
        timezone,
        time(17, 30),
        timedelta(minutes=100),
        "AtCoder Beginner Contest",
        "Weekly AtCoder Beginner Contest.",
    )

    if len(calendar.events) == before_count:
        print("No AtCoder contests were added to the calendar.")
        return False

    return True


def next_biweekly_anchor(today: date) -> date:
    anchor = date(2024, 10, 11)
    while anchor <= today:
        anchor += timedelta(days=14)
    return anchor


def handle_leetcode(reminder_minutes: int, calendar: Calendar) -> bool:
    timezone = tz.gettz("Asia/Kolkata")
    if timezone is None:
        print("Unable to load Asia/Kolkata timezone data.")
        return False

    today = datetime.now(timezone).date()
    end_date = today + relativedelta(months=+6)

    first_weekly = next_weekday(today, 6)  # Sunday
    first_biweekly = next_biweekly_anchor(today)
    before_count = len(calendar.events)

    if first_weekly <= end_date:
        generate_weekly_events(
            calendar,
            first_weekly,
            end_date,
            timezone,
            time(8, 0),
            timedelta(minutes=90),
            "LeetCode Weekly Contest",
            "LeetCode Weekly Contest.",
        )

    if first_biweekly <= end_date:
        current = first_biweekly
        while current <= end_date:
            start_dt = datetime.combine(current, time(20, 0), tzinfo=timezone)
            if start_dt.weekday() != 5:  # ensure Saturday
                offset = (5 - start_dt.weekday()) % 7
                start_dt += timedelta(days=offset)
            event = Event(
                name="LeetCode Biweekly Contest",
                begin=start_dt,
                end=start_dt + timedelta(minutes=90),
                description="LeetCode Biweekly Contest.",
            )
            calendar.events.add(event)
            current = current + timedelta(days=14)

    if len(calendar.events) == before_count:
        print("No LeetCode contests fall within the provided range.")
        return False

    return True


def main() -> None:
    platforms: Dict[str, Tuple[str, PlatformHandler]] = {
        "codeforces": ("Codeforces", handle_codeforces),
        "codechef": ("CodeChef", handle_codechef),
        "atcoder": ("AtCoder", handle_atcoder),
        "leetcode": ("LeetCode", handle_leetcode),
    }

    platform_labels = {key: label for key, (label, _) in platforms.items()}
    selected_keys = prompt_menu_choices(platform_labels)
    reminder_minutes = prompt_non_negative_int(
        "Reminder lead time in minutes before the contest (default 10): ", default=10
    )

    aggregated_calendar = Calendar()
    successful_platforms: List[str] = []

    for key in selected_keys:
        label, handler = platforms[key]
        if handler(reminder_minutes, aggregated_calendar):
            successful_platforms.append(key)

    if not aggregated_calendar.events:
        print("No contests were added for the selected platforms.")
        return

    short_names = {
        "codeforces": "CF",
        "codechef": "CC",
        "atcoder": "AC",
        "leetcode": "LC",
    }

    platforms_for_name = successful_platforms or selected_keys
    platform_suffix = "_".join(short_names[key] for key in platforms_for_name)
    today_str = datetime.now(tz.tzlocal()).date().isoformat()
    filename = f"{today_str}_{platform_suffix}.ics"

    ics_text = inject_alarms(aggregated_calendar.serialize(), reminder_minutes)

    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(ics_text)
    except OSError as error:
        print(f"Failed to write {filename}: {error}")
        return

    print(f"\nCalendar file created: {filename}")
    print("Import this file into your calendar application to add the contests.")


if __name__ == "__main__":
    main()
