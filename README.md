# Contest Calendar

Generate iCalendar (`.ics`) files for competitive programming contests across multiple platforms. The single entry-point script `contest_calendar.py` lets you build a combined calendar with reminder alarms, supports both interactive and non-interactive runs, and is ready for automation (for example via cron) so your Codeforces schedule stays up to date.

## Supported Platforms

- **Codeforces** – fetched via the public API and deduplicated when multiple divisions begin at the same time. Events use stable UIDs so re-importing updates existing entries.
- **CodeChef** – weekly recurring contests projected six months into the future.
- **AtCoder** – weekly Beginner Contests projected six months into the future.
- **LeetCode** – weekly and biweekly contests projected six months into the future.

All events include a reminder alert (`VALARM`) that fires before the start time. You control the reminder lead time when running the script.

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`:
  - `requests`
  - `ics`
  - `python-dateutil`

Install them with:

```bash
pip install -r requirements.txt
```

## Usage

### Interactive run

```bash
python3 contest_calendar.py
```

You will be prompted to choose one or more platforms and to set the reminder lead time (default: 10 minutes). The script writes a single `.ics` file named `<today>_<platform-codes>.ics` (for example `2025-10-05_CF_CC_AC.ics`).

### Non-interactive run (CLI flags)

```bash
python3 contest_calendar.py \
  --platforms cf,lc \
  --reminder 30 \
  --output contest_calendar.ics \
  --quiet \
  --open
```

Useful flags:

- `--platforms` &ndash; comma or space separated platform codes (`cf`, `cc`, `ac`, `lc`). When omitted, you will be prompted interactively.
- `--reminder` &ndash; reminder lead time in minutes (must be ≥ 0).
- `--output` &ndash; custom output path for the resulting `.ics` file.
- `--quiet` &ndash; suppress informational logs (recommended for cron jobs).
- `--open` &ndash; open the generated file with the default handler (macOS `open`).

### Automating a weekly Codeforces refresh

1. Make the helper script executable:

   ```bash
   chmod +x update_codeforces_calendar.sh
   ```

2. Add a cron entry to rebuild and import the Codeforces calendar every Sunday at 9 AM (adjust the schedule or paths as needed):

   ```cron
   0 9 * * 0 /bin/bash /Users/86pushkar24/Desktop/Archive/Calendar/update_codeforces_calendar.sh >> /Users/86pushkar24/Desktop/Archive/Calendar/contest_calendar_cron.log 2>&1
   ```

The helper script calls the main generator with `--platforms codeforces --quiet`, produces `codeforces_contests.ics`, and reopens the file so Calendar replaces existing events (thanks to the deterministic UIDs).

## Customisation

- **Reminder lead time** &ndash; change via `--reminder` or edit the default in `contest_calendar.py:499-502`.
- **Forecast window** &ndash; each recurring handler projects six months ahead; adjust the `relativedelta(months=+6)` assignments in the platform handlers (see `contest_calendar.py:327-418`).
- **Output naming** &ndash; tweak the filename construction in `contest_calendar.py:520-525` if a different naming pattern suits your workflow.

## Calendar details

- Every event stores a stable `UID`, so importing the updated file replaces existing entries instead of creating duplicates.
- Reminder alarms are injected directly into each `VEVENT` (`VALARM` display notifications).
- Codeforces contests are grouped by start time; additional divisions are listed in the description rather than added as separate events.

## Repository layout

```
Calendar/
├── README.md
├── contest_calendar.py
├── requirements.txt
└── update_codeforces_calendar.sh
```

## Development

- Run `python3 -m py_compile contest_calendar.py` to perform a quick syntax check.
- Linting/tests are not bundled; feel free to integrate your preferred tooling.
- The project intentionally limits dependencies to keep cron/automation environments simple.
