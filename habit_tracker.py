import os
import datetime
import matplotlib.pyplot as plt
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class HabitTracker:
    def __init__(self, habit_name, user_email):
        self.habit_name = habit_name
        self.user_email = user_email
        self.habit_data = self.load_habit_data()
    
    def load_habit_data(self):
        if not os.path.exists('habit_data.txt'):
            return {}
        with open('habit_data.txt', 'r') as f:
            lines = f.readlines()
        habit_data = {}
        for line in lines:
            date, status = line.strip().split(',')
            habit_data[date] = status
        return habit_data
    
    def save_habit_data(self):
        with open('habit_data.txt', 'w') as f:
            for date, status in self.habit_data.items():
                f.write(f"{date},{status}\n")
    
    def log_habit(self):
        date = datetime.date.today().strftime("%Y-%m-%d")
        status = input(f"Did you complete your habit '{self.habit_name}' today? (y/n): ").strip().lower()
        if status in ['y', 'n']:
            self.habit_data[date] = status
            self.save_habit_data()
            print(f"Logged habit for {date}.")
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
    
    def visualize_progress(self):
        dates = list(self.habit_data.keys())
        statuses = [1 if self.habit_data[date] == 'y' else 0 for date in dates]
        x = np.arange(len(dates))

        plt.figure(figsize=(10, 6))
        plt.bar(x, statuses, tick_label=dates)
        plt.xlabel('Date')
        plt.ylabel('Habit Completed (1 = Yes, 0 = No)')
        plt.title(f"Progress for Habit: {self.habit_name}")
        plt.xticks(rotation=45, ha='right')
        plt.show()
    
    def send_reminder(self):
        message = MIMEMultipart()
        message['From'] = 'your_email@gmail.com'
        message['To'] = self.user_email
        message['Subject'] = f"Reminder: Track Your Habit - {self.habit_name}"

        body = f"Hi! Just a reminder to track your habit '{self.habit_name}' today."
        message.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login('your_email@gmail.com', 'your_password')  # Use an App Password if 2FA is enabled
            server.sendmail(message['From'], message['To'], message.as_string())
            server.quit()
            print("Reminder email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")

if __name__ == "__main__":
    habit_name = input("Enter the name of the habit: ").strip()
    user_email = input("Enter your email for daily reminders: ").strip()
    
    tracker = HabitTracker(habit_name, user_email)
    
    while True:
        print("\nOptions:")
        print("1. Log Habit")
        print("2. Visualize Progress")
        print("3. Send Daily Reminder")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            tracker.log_habit()
        elif choice == '2':
            tracker.visualize_progress()
        elif choice == '3':
            tracker.send_reminder()
        elif choice == '4':
            print("Exiting Habit Tracker. Goodbye!")
            break
        else:
            print("Invalid choice, please select a valid option.")
