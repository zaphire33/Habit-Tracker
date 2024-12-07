from habit_tracker import HabitTracker


def send_daily_reminder():
    habit_name = "Exercise"
    user_email = "user_email@example.com"
    tracker = HabitTracker(habit_name, user_email)
    tracker.send_reminder()

send_daily_reminder()
