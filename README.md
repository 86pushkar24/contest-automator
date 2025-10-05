# Contest Calendar Generator

An interactive Python utility that assembles upcoming programming contest schedules from popular platforms into an iCalendar (`.ics`) file you can import into Google Calendar, Apple Calendar, or any modern calendar app. The tool mixes live data (Codeforces) with well-known recurring contest slots (CodeChef, AtCoder, LeetCode) so you can keep an eye on weekly and biweekly rounds without manually creating events.

## Features
- Supports Codeforces, CodeChef, AtCoder, and LeetCode with simple aliases (`cf`, `cc`, `ac`, `lc`).
- Interactive menu when no platforms are specified; fully scriptable via CLI flags.
- Fetches Codeforces contest data through the public API and groups overlapping divisions into a single event per timeslot.
- Generates recurring events for the other platforms in the Asia/Kolkata timezone for the next six months.
- Injects meeting reminders into every event (10 minutes by default, configurable per run).
- Produces self-contained `.ics` files with deterministic filenames and optional automatic opening on macOS.

## Requirements
- Python 3.8 or newer (relies on postponed annotations from `__future__`).
- Dependencies listed in `requirements.txt`:
  - `requests` for HTTP access to the Codeforces API.
  - `ics` for building iCalendar files.
  - `python-dateutil` for timezone handling and recurring date math.

Install dependencies with:

```bash
python3 -m pip install -r requirements.txt
```

## Getting Started
1. Clone or download this repository.
2. (Optional) Create and activate a virtual environment.
3. Install dependencies as shown above.
4. Run the generator:

   ```bash
   python3 contest_calendar.py
   ```

   The script will prompt you to select platforms and reminder lead time if you do not pass flags.

## Command-Line Usage
You can bypass the interactive prompts and automate runs with CLI options:

```bash
python3 contest_calendar.py \
  --platforms cf,lc \
  --reminder 15 \
  --output my_contests.ics \
  --open
```

- `--platforms`: Comma/space separated list. Aliases: `cf`, `cc`, `ac`, `lc`.
- `--reminder`: Minutes before contest start to trigger an alert (must be ≥ 0).
- `--output`: Custom output file name. Defaults to `YYYY-MM-DD_CF_CC.ics` based on the selected platforms.
- `--quiet`: Suppress non-error console output (useful for scheduled jobs).
- `--open`: Open the generated file with the default system handler (designed for macOS `open`).

If you omit `--platforms` or `--reminder`, the script falls back to prompting in the terminal for those values.

## Platform Schedules
- **Codeforces**: Retrieves upcoming contests from the official API. When multiple divisions overlap, the script keeps the most relevant division (preferring Div. 2 → Div. 3 → Div. 4 → Div. 1) and lists the rest in the event description.
- **CodeChef**: Creates weekly events every Wednesday at 20:00 Asia/Kolkata with a 2-hour duration.
- **AtCoder**: Creates weekly events every Saturday at 17:30 Asia/Kolkata lasting 100 minutes for the Beginner Contest.
- **LeetCode**: Creates weekly contests every Sunday at 08:00 Asia/Kolkata and biweekly contests every other Saturday night at 20:00 Asia/Kolkata.

All recurring schedules are generated for the six months following the run date. Adjust the source code if you would like to target a different timezone or cadence.

## Automating Codeforces Updates (macOS)
The helper script `update_codeforces_calendar.sh` regenerates a Codeforces-only calendar and opens it in the Calendar app:

```bash
./update_codeforces_calendar.sh
```

It runs the main generator with `--platforms codeforces`, a 10-minute reminder, and saves the result as `codeforces_contests.ics` alongside the script. Feel free to adapt this script for other platforms or scheduling tools.

## Importing the Calendar
1. Run the generator to create an `.ics` file.
2. Import the file into your calendar application (drag-and-drop into Apple Calendar, or use "Import" in Google Calendar / Outlook).
3. Verify that the events and reminder times appear as expected.

## Troubleshooting
- **No Codeforces events**: The API occasionally returns no upcoming contests; rerun later or confirm on the Codeforces website.
- **Timezone differences**: Static schedules use Asia/Kolkata. Edit the handler functions in `contest_calendar.py` to use a different region if needed.
- **ICS file not opening**: Use the `--open` flag on macOS, or double-click the generated file manually on other platforms.

## Contributing / Extending
The code is organized by platform-specific handler functions in `contest_calendar.py`. To add a new platform:
1. Implement a handler matching the signature `(reminder_minutes, calendar, quiet) -> bool`.
2. Register the handler in the `platforms` dictionary.
3. Add an alias in `PLATFORM_ALIASES` if you want shorthand support.
4. Update this README with details for the new platform.

Pull requests and suggestions for more accurate recurring schedules are welcome.
