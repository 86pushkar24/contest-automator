import requests
from ics import Calendar, Event
from datetime import datetime, timedelta
import subprocess
import os

# ========== Step 1: Fetch Upcoming Contests ==========
def fetch_upcoming_contests(limit=5):
    url = "https://codeforces.com/api/contest.list"
    print("Fetching contests from Codeforces...")
    response = requests.get(url).json()

    if response["status"] != "OK":
        raise Exception("Failed to fetch contests from Codeforces API.")

    contests = response["result"]
    
    # Filter for only upcoming Codeforces (CF) contests
    upcoming = [
        c for c in contests
        if c["phase"] == "BEFORE" and c["type"] == "CF" and "startTimeSeconds" in c
    ]

    return upcoming[:limit]

# ========== Step 2: Convert Contests to ICS ==========
def generate_ics(contests):
    calendar = Calendar()
    print("Generating .ics calendar entries...")

    for contest in contests:
        event = Event()
        event.name = contest["name"]

        start_time = datetime.utcfromtimestamp(contest["startTimeSeconds"])
        duration = timedelta(seconds=contest["durationSeconds"])
        url = f'https://codeforces.com/contest/{contest["id"]}'

        description_lines = [
            f"🧭 Type: {contest.get('kind', 'Codeforces Round')}",
            f"🎯 Difficulty: {contest.get('difficulty', 'N/A')}",
            f"⏱ Duration: {duration}",
            f"🔗 URL: {url}"
        ]

        if "websiteUrl" in contest:
            description_lines.append(f"🌐 Website: {contest['websiteUrl']}")
        if "city" in contest:
            description_lines.append(f"📍 City: {contest['city']}")
        if "country" in contest:
            description_lines.append(f"🌎 Country: {contest['country']}")
        if "icpcRegion" in contest:
            description_lines.append(f"🏅 ICPC Region: {contest['icpcRegion']}")

        event.begin = start_time
        event.duration = duration
        event.url = url
        event.description = "\n".join(description_lines)

        calendar.events.add(event)

    # Convert to .ics string
    ics_text = str(calendar)

    # Inject a 15-minute VALARM before each event
    alarm_block = (
        "BEGIN:VALARM\n"
        "TRIGGER:-PT15M\n"
        "ACTION:DISPLAY\n"
        "DESCRIPTION:Reminder\n"
        "END:VALARM"
    )

    # Add the alarm block into each VEVENT
    ics_text_with_alarms = ics_text.replace("END:VEVENT", alarm_block + "\nEND:VEVENT")

    return ics_text_with_alarms


# ========== Step 3: Save to ICS File ==========
def save_ics(data, filename="codeforces_contests.ics"):
    print(f"Saving calendar file to {filename}...")
    with open(filename, "w") as file:
        file.write(data)
    return os.path.abspath(filename)

# ========== Step 4: Open with Apple Calendar ==========
def open_in_calendar(filepath):
    print("Opening calendar file in Apple Calendar...")
    subprocess.run(["open", filepath])

# ========== Main Function ==========
def main():
    try:
        contests = fetch_upcoming_contests()
        if not contests:
            print("No upcoming Codeforces contests found.")
            return

        ics_data = generate_ics(contests)
        filepath = save_ics(ics_data)
        open_in_calendar(filepath)

        print("✅ Codeforces contests successfully added to Apple Calendar!")

    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    main()
