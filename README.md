# Habit Tracker Django Application

A web application built with Django that helps users build consistent routines, track daily habit completions, monitor streaks, and organize habits by category.

---

## Features

- **User Authentication & Profiles**: User signup, login/logout, and personal profile management with customizable profile pictures and contact information.
- **Habit Management**: Create, view, and organize habits into custom categories[cite: 1].
- **Streak & Progress Tracking**: Real-time tracking of current and maximum streak records per habit[cite: 1].
- **Daily Logs & History**: Dedicated log history recording dates and completion status[cite: 1].
- **Analytics & Reports**: Visual reports and breakdown of your habit consistency over time[cite: 1].
- **Deployment Ready**: Configured with a `Procfile` for production deployment using Gunicorn[cite: 1].

---

## Project Structure

```text
habit-tracker-django/
│
├── habitTracker/             # Project configuration directory[cite: 1]
│   ├── asgi.py[cite: 1]
│   ├── settings.py[cite: 1]
│   ├── urls.py[cite: 1]
│   └── wsgi.py[cite: 1]
│
├── myapp/                    # Core application directory[cite: 1]
│   ├── migrations/           # Database schema migrations[cite: 1]
│   ├── static/               # Static assets (CSS stylesheets)[cite: 1]
│   ├── templates/            # HTML templates (auth, habits, categories, reports)[cite: 1]
│   ├── admin.py              # Django admin registrations[cite: 1]
│   ├── forms.py              # User and habit form validations[cite: 1]
│   ├── models.py             # Database models (Habit, HabitLog, HabitCategory, Profile)[cite: 1]
│   ├── urls.py               # App route definitions[cite: 1]
│   └── views.py              # Application controller logic[cite: 1]
│
├── media/                    # User-uploaded media (profile pictures)[cite: 1]
├── manage.py                 # Django management script[cite: 1]
├── Procfile                  # Deployment process definition (Gunicorn)[cite: 1]
├── requirements.txt          # Python dependencies[cite: 1]
└── .gitignore                # Ignored version control patterns[cite: 1]
