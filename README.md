# ⏳ Pomodoro Timer with MySQL Productivity Tracker

A feature-rich **Pomodoro Timer** built using Python's `tkinter` for GUI and `mysql-connector-python` for real-time productivity tracking. This tool helps you manage your work sessions, keep track of time spent, and auto-log your daily productivity into a MySQL database.

---

## 🎯 Features

- ✅ Follows Pomodoro Technique (25 mins work, 5 mins short break, 20 mins long break)
- ✅ Automatically cycles between work and break sessions
- ✅ MySQL integration to record and update total daily work hours
- ✅ Real-time display of completed sessions with checkmarks (🗸)
- ✅ Timer control buttons: Start, Stop, Reset
- ✅ Uses system sounds to alert on session switches

---

## 🖼️ UI Preview

![Pomodoro Timer UI](.venv/img.png)

---

## 📦 Requirements

- Python 3.x
- `mysql-connector-python`  
- MySQL server running with:
  - Database: `daily_pomodoro`
  - Table: `report(date DATE PRIMARY KEY, total_duration_hrs FLOAT)`
- Image file: `tomato.png` (placed in the same directory)

### Python Packages

Install required package:

```bash
pip install mysql-connector-python
