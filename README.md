# Contest Automator

Automatically fetch upcoming Codeforces contests and add them to your Apple Calendar with reminders.

## Features

- 🔄 **Automatic Contest Fetching**: Retrieves upcoming Codeforces contests via API
- 📅 **Calendar Integration**: Generates .ics files compatible with Apple Calendar
- ⏰ **Smart Reminders**: Adds 15-minute alerts before each contest
- 📝 **Rich Details**: Includes contest type, duration, difficulty, and direct links
- 🎯 **Filtered Results**: Shows only upcoming CF (Codeforces) rounds

## Requirements

- Python 3.6+
- Internet connection (for Codeforces API)
- macOS (for automatic Apple Calendar integration)

## Installation

1. **Clone or download** this project to your local machine

2. **Navigate to the project directory**:

   ```bash
   cd ~/Desktop/Archive/Calendar
   ```

3. **Create a virtual environment** (recommended):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   # or
   . .venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   pip install --upgrade pip setuptools wheel
   pip install requests ics
   ```

## Usage

### Interactive run

Launch the unified generator and pick platforms when prompted:

```bash
python3 contest_calendar.py
```

You will choose the contest platforms (Codeforces, CodeChef, AtCoder, LeetCode) and set a reminder lead time. The script writes a single ICS file containing all selected events.

### Non-interactive run

Use command-line flags to automate generation (ideal for cron jobs):

```bash
python3 contest_calendar.py \
  --platforms cf \
  --reminder 10 \
  --output contest_calendar.ics \
  --quiet
```

Short codes: `cf` (Codeforces), `cc` (CodeChef), `ac` (AtCoder), `lc` (LeetCode). Add `--open` to automatically import the resulting file into Apple Calendar.

### Automating a weekly Codeforces refresh

1. Make the helper script executable:

   ```bash
   chmod +x update_codeforces_calendar.sh
   ```

2. Add a cron entry to rebuild the ICS every Sunday at 9 AM and re-import it:

   ```cron
   0 9 * * 0 /bin/bash /Users/86pushkar24/Desktop/Archive/Calendar/update_codeforces_calendar.sh >> /Users/86pushkar24/Desktop/Archive/Calendar/contest_calendar_cron.log 2>&1
   ```

   Adjust the path or schedule to suit your setup. The helper script generates `codeforces_contests.ics` with stable UIDs so Calendar replaces existing events when the file is reopened.

## Customization

- Change the reminder lead time with the `--reminder` flag or by editing the
  default prompt in `contest_calendar.py:493-502`.
- Adjust the coverage window for recurring contests inside each handler (for
  example the six-month span at `contest_calendar.py:327-370`).
- Override the output filename with `--output` or by modifying the naming logic
  in `contest_calendar.py:519-525`.

## File Structure

```
Contest-Automator/
├── README.md                         # Project documentation
├── contest_calendar.py               # Unified multi-platform generator
├── update_codeforces_calendar.sh     # Weekly automation helper for cron
├── atcoder_calendar.py               # Legacy single-platform script (optional)
├── codechef_calendar.py              # Legacy single-platform script (optional)
├── codeforces_calendar.py            # Legacy single-platform script (optional)
├── leetcode_calendar.py              # Legacy single-platform script (optional)
└── requirements.txt                  # Dependencies (optional)
```

## Generated Calendar Events

Each contest event includes:

- **Title**: Contest name (e.g., "Codeforces Round 906 (Div. 2)")
- **Date/Time**: Contest start time in your local timezone
- **Duration**: Exact contest duration
- **Description**:
  - Contest type and difficulty
  - Duration details
  - Direct contest URL
  - Additional metadata (city, country, ICPC region if available)
- **Reminder**: 15-minute alert before start time

## Troubleshooting

### Common Issues

**"Package not found" error**:

```bash
# Install missing packages
pip install requests ics
```

**"Failed to fetch contests" error**:

- Check your internet connection
- Verify Codeforces API is accessible: `curl https://codeforces.com/api/contest.list`

**Calendar doesn't open automatically**:

- The script uses macOS `open` command
- On Linux, modify `open_in_calendar()` to use `xdg-open`
- On Windows, use `start` command

**SSL/TLS warnings**:

- These are harmless warnings about urllib3 and LibreSSL
- The script will work normally despite the warnings

### Platform Compatibility

**macOS** ✅: Full support with automatic Calendar.app integration

**Linux** ⚠️: Manual modification needed:

```python
def open_in_calendar(filepath):
    subprocess.run(["xdg-open", filepath])
```

**Windows** ⚠️: Manual modification needed:

```python
def open_in_calendar(filepath):
    subprocess.run(["start", filepath], shell=True)
```

## Dependencies

- `requests`: HTTP library for API calls
- `ics`: Python library for generating iCalendar files
- `python-dateutil`: Date/time parsing (installed with `ics`)

## API Information

This project uses the official [Codeforces API](https://codeforces.com/apiHelp):

- **Endpoint**: `https://codeforces.com/api/contest.list`
- **Rate Limits**: Codeforces API has reasonable rate limits for personal use
- **Data**: Public contest information (no authentication required)

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for improvements:

- Add support for other competitive programming platforms
- Implement command-line arguments
- Add configuration file support
- Improve cross-platform compatibility

## License

This project is provided as-is for educational and personal use. Please respect Codeforces' terms of service when using their API.

---

**Happy Coding! 🚀**

_Never miss a contest again with Contest Automator_
