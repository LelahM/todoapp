# GetTasked - Todo Application

A beautiful and feature-rich task management application built with Flask.

## 🚀 Quick Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/LelahM/todoapp)

## Features

- Task organization by categories (Work, School, Personal, Other)
- Priority levels (High, Medium, Low)
- Due date reminders with visual indicators
- Task notes/descriptions
- Task sorting options
- Progress tracking with affirmations
- Interactive charts for progress visualization
- Browser notifications for upcoming tasks
- User personalization

## Running Locally

1. Make sure you have Python 3.8+ installed

2. Run the application:
   ```
   ./run.sh
   ```

3. Open your browser and go to:
   [http://localhost:5001](http://localhost:5001)

## Deployment Options

### Option 1: Render.com (Free Tier)

1. Sign up for a free account at [Render.com](https://render.com)
2. Create a new Web Service
3. Connect your GitHub repository
4. Set the build command: `pip install -r requirements.txt`
5. Set the start command: `gunicorn app:app`

### Option 2: PythonAnywhere (Free Tier)

1. Sign up at [PythonAnywhere.com](https://www.pythonanywhere.com)
2. Upload your files using the Files tab
3. Create a new web app with Flask
4. Configure the WSGI file to point to your app.py

### Option 3: Heroku (Paid)

1. Install Heroku CLI
2. Create a Procfile with: `web: gunicorn app:app`
3. Run:
   ```
   heroku login
   heroku create
   git push heroku main
   ```

## License

MIT
