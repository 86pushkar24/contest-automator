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

### Quick Start

Run the script to fetch the next 5 upcoming contests:

```bash
python3 codeforces_calendar.py
```

### What It Does

1. **Fetches Contests**: Connects to `https://codeforces.com/api/contest.list`
2. **Filters**: Shows only upcoming CF contests with valid start times
3. **Generates Calendar**: Creates `codeforces_contests.ics` in the project directory
4. **Opens Calendar**: Automatically launches Apple Calendar to import events

### Example Output

```
Fetching contests from Codeforces...
Generating .ics calendar entries...
Saving calendar file to codeforces_contests.ics...
Opening calendar file in Apple Calendar...
✅ Codeforces contests successfully added to Apple Calendar!
```

## Customization

### Change Contest Limit

Edit `codeforces_calendar.py` and modify the `main()` function:

```python
def main():
    contests = fetch_upcoming_contests(limit=10)  # Get 10 contests instead of 5
    # ... rest of the code
```

### Custom Output Filename

Modify the `save_ics()` call in `main()`:

```python
filepath = save_ics(ics_data, "my_contests.ics")
```

### Disable Auto-Open

Comment out or remove this line in `main()`:

```python
# open_in_calendar(filepath)  # Disable auto-open
```

## File Structure

```
Contest-Automator/
├── README.md                    # This file
├── codeforces_calendar.py      # Main script
├── codeforces_contests.ics     # Generated calendar file
├── .venv/                      # Virtual environment (created after setup)
└── requirements.txt            # Dependencies (optional)
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
