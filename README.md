# 🏆 Contest Calendar Generator

<div align="center">

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platforms](https://img.shields.io/badge/platforms-CF%20%7C%20CC%20%7C%20AC%20%7C%20LC-orange.svg)](#supported-platforms)

_Never miss a programming contest again!_ 📅

</div>

An interactive Python utility that automatically generates calendar files for upcoming programming contests from popular platforms. Simply run the script and import the generated `.ics` file into your favorite calendar app to stay on top of all contests!

## ✨ Why Use This Tool?

- 🎯 **One-click setup**: Generate calendar events for all major programming platforms
- 🔄 **Always up-to-date**: Fetches live contest data from APIs
- ⏰ **Smart reminders**: Never miss a contest with customizable alerts
- 📱 **Universal compatibility**: Works with Google Calendar, Apple Calendar, Outlook, and more
- 🚀 **Easy automation**: Perfect for competitive programmers and contest enthusiasts

## 🎪 Supported Platforms

| Platform       | Alias | Schedule                        | Duration    |
| -------------- | ----- | ------------------------------- | ----------- |
| **Codeforces** | `cf`  | Live API data                   | Variable    |
| **CodeChef**   | `cc`  | Wednesdays 8:00 PM IST          | 2 hours     |
| **AtCoder**    | `ac`  | Saturdays 5:30 PM IST           | 100 minutes |
| **LeetCode**   | `lc`  | Sundays 8:00 AM IST + Bi-weekly | 90 minutes  |

## ✨ Key Features

- 🎯 **Multi-platform support** with simple aliases (`cf`, `cc`, `ac`, `lc`)
- 🤖 **Interactive mode** with guided setup or **CLI automation** for power users
- 📊 **Smart contest grouping** - combines overlapping divisions into single events
- ⏰ **Customizable reminders** (10 minutes default, fully adjustable)
- 📅 **Flexible time horizon** - generate up to 6 months of contests
- 🍎 **macOS integration** - automatically opens generated calendars
- 🔧 **Developer-friendly** - easy to extend with new platforms

## 🚀 Quick Start

### Prerequisites

- 🐍 **Python 3.8+** (uses modern type annotations)
- 📦 **pip** (Python package manager)

### 📥 Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd contest-calendar-generator
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   <details>
   <summary>📋 What gets installed?</summary>

   - `requests` - For fetching contest data from APIs
   - `ics` - For creating calendar files
   - `python-dateutil` - For smart date/time handling

   </details>

3. **Run the generator**
   ```bash
   python3 contest_calendar.py
   ```

That's it! 🎉 The script will guide you through the rest.

## 💡 Usage Examples

### 🎮 Interactive Mode (Recommended for beginners)

Simply run the script and follow the prompts:

```bash
python3 contest_calendar.py
```

The tool will ask you:

- Which platforms to include
- How many minutes before contests to remind you
- How many months of contests to generate

### ⚡ Command-Line Mode (For power users)

**Generate contests for all platforms with 15-minute reminders:**

```bash
python3 contest_calendar.py --platforms cf,cc,ac,lc --reminder 15 --months 6
```

**Quick Codeforces-only calendar:**

```bash
python3 contest_calendar.py --platforms cf --reminder 10 --months 3 --open
```

**Silent mode for automation:**

```bash
python3 contest_calendar.py --platforms cf,lc --reminder 5 --months 4 --quiet
```

### 🛠️ Command-Line Options

| Option        | Description                                   | Example                    |
| ------------- | --------------------------------------------- | -------------------------- |
| `--platforms` | Platforms to include (`cf`, `cc`, `ac`, `lc`) | `--platforms cf,lc`        |
| `--reminder`  | Minutes before contest for alerts             | `--reminder 15`            |
| `--months`    | Months of contests to generate                | `--months 6`               |
| `--output`    | Custom output filename                        | `--output my_contests.ics` |
| `--quiet`     | Suppress console output                       | `--quiet`                  |
| `--open`      | Auto-open file (macOS)                        | `--open`                   |

## 📅 How It Works

### 🎯 Smart Contest Detection

- **Codeforces**: Fetches live contest data from the official API
- **Other Platforms**: Uses well-known recurring schedules

### 🧠 Intelligent Grouping

When multiple Codeforces divisions overlap (e.g., Div. 1 + Div. 2), the tool:

1. Creates one event for the most relevant division (Div. 2 → Div. 3 → Div. 4 → Div. 1)
2. Lists other divisions in the event description
3. Keeps your calendar clean and organized

### 🌍 Timezone & Scheduling

All contests are scheduled in **Asia/Kolkata timezone**:

<details>
<summary>📊 Detailed Platform Schedules</summary>

| Platform       | When                                          | Duration    | Notes                      |
| -------------- | --------------------------------------------- | ----------- | -------------------------- |
| **Codeforces** | Variable (API-driven)                         | 2-3 hours   | Live contest data          |
| **CodeChef**   | Every Wednesday 8:00 PM                       | 2 hours     | Long Challenge + Cook-offs |
| **AtCoder**    | Every Saturday 5:30 PM                        | 100 minutes | Beginner Contest           |
| **LeetCode**   | Sundays 8:00 AM + Bi-weekly Saturdays 8:00 PM | Variable    | Weekly + Bi-weekly rounds  |

</details>

## 📱 Adding to Your Calendar

### Method 1: Drag & Drop (Easiest)

1. Run the script to generate your `.ics` file
2. Drag the file directly into your calendar app
3. ✅ Done! Your contests are now scheduled

### Method 2: Import Feature

1. Open your calendar app (Google Calendar, Apple Calendar, Outlook, etc.)
2. Find the "Import" or "Add Calendar" option
3. Select your generated `.ics` file
4. Choose calendar settings and confirm

### Method 3: Auto-open (macOS)

Use the `--open` flag to automatically open the calendar file:

```bash
python3 contest_calendar.py --platforms cf --open
```

## 🔄 Automation & Scheduling

### 🍎 macOS Quick Update Script

For Codeforces enthusiasts, use the included helper script:

```bash
./update_codeforces_calendar.sh
```

This script:

- ⚡ Generates a Codeforces-only calendar
- 🔔 Sets 10-minute reminders
- 📅 Auto-opens in Calendar app
- 💾 Saves as `codeforces_contests.ics`

### 🔧 Custom Automation

Create your own automation by adapting the script for different platforms or adding it to cron jobs for regular updates.

## 🔧 Troubleshooting

<details>
<summary>❌ Common Issues & Solutions</summary>

### No Codeforces Events Showing

- **Cause**: API temporarily unavailable or no upcoming contests
- **Solution**: Wait and rerun, or check [codeforces.com](https://codeforces.com) directly

### Calendar File Won't Open

- **Cause**: System doesn't know how to handle `.ics` files
- **Solution**:
  - Use `--open` flag on macOS
  - Manually drag file into calendar app
  - Right-click → "Open with" → Calendar app

### Wrong Timezone

- **Current**: All times in Asia/Kolkata (IST)
- **Solution**: Edit platform handlers in `contest_calendar.py` for different timezone

### Missing Dependencies

- **Error**: `ModuleNotFoundError`
- **Solution**: Run `pip install -r requirements.txt`

</details>

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### 🆕 Adding New Platforms

1. **Create handler function** in `contest_calendar.py`:

   ```python
   def handle_platform_name(reminder_minutes, months_ahead, calendar, quiet):
       # Your implementation here
       return True  # Success
   ```

2. **Register the platform**:

   ```python
   platforms = {
       'platform_name': handle_platform_name,
       # ... existing platforms
   }
   ```

3. **Add alias** (optional):

   ```python
   PLATFORM_ALIASES = {
       'pn': 'platform_name',  # Short alias
       # ... existing aliases
   }
   ```

4. **Update this README** with the new platform details

### 🐛 Bug Reports & Feature Requests

- Open an issue with detailed description
- Include error messages and system info
- Suggest improvements for better contest schedules

### 📝 Documentation

- Fix typos or unclear instructions
- Add examples for new use cases
- Improve platform-specific guidance

---

<div align="center">

**Made with ❤️ for competitive programmers**

_Never miss another contest! 🚀_

[⭐ Star this repo](../../stargazers) if it helped you stay on top of your programming contests!

</div>
