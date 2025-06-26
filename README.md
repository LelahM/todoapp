# GetTasked - Modern Task Management Application

A beautiful, feature-rich task management application built with Flask, featuring a stunning glassmorphism UI design and comprehensive productivity tools.

## 🌐 Live Demo

**🚀 [Try GetTasked Live on Vercel](https://gettasked.vercel.app)**

Experience the full-featured todo application with real-time task management, progress tracking, and beautiful visualizations.

## ✨ Features

### 📋 **Task Management**
- ✅ Create, edit, delete, and toggle tasks
- 🏷️ **Categories**: Work, School, Personal, Shopping, Other
- ⭐ **Priority Levels**: High, Medium, Low
- 📝 **Task Notes**: Add detailed descriptions
- 📅 **Due Dates**: Set deadlines with smart reminders

### 🎨 **Beautiful UI Design**
- 🌊 **Glassmorphism Design**: Modern, translucent interface
- 📱 **Fully Responsive**: Perfect on desktop, tablet, and mobile
- ✨ **Smooth Animations**: Engaging user interactions
- 🎯 **Intuitive Layout**: Easy-to-use interface

### 📊 **Progress Tracking**
- 📈 **Interactive Charts**: Visual progress with Chart.js
- 💪 **Motivational Messages**: Personalized encouragement
- 📊 **Completion Statistics**: Track your productivity
- 🎯 **Category Analytics**: See progress by task type

### ⏰ **Smart Reminders**
- 🚨 **Overdue Tasks**: Never miss important deadlines
- 📅 **Due Today**: Focus on today's priorities  
- ⏰ **Due Soon**: Upcoming tasks (next 24 hours)
- 📆 **Due This Week**: Weekly planning overview

### 👤 **Personalization**
- 🏷️ **Custom Username**: Personalized experience
- 🎨 **Theme Consistency**: Beautiful color coordination
- 💾 **Session Storage**: Maintains state during use

## 🚀 Quick Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/LelahM/todoapp)

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Charts**: Chart.js
- **Styling**: Custom CSS with Glassmorphism
- **Icons**: Unicode Emojis
- **Deployment**: Vercel (Serverless)
- **Storage**: In-memory (demo) / SQLite (local)

## 📊 Database Structure

### User Model
```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, default="Friend")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tasks = db.relationship('Task', backref='user', lazy=True)
```

### Task Model
```python
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.String(10), nullable=False, default="medium")
    notes = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
```

## 🏗️ Project Architecture

```
GetTasked/
├── app.py              # Main Flask application
├── app_simple.py       # Simplified version for serverless
├── index.py            # Vercel entry point
├── config.py           # Configuration settings
├── models.py           # Database models
├── static/             # Static assets
│   ├── css/            # CSS stylesheets
│   ├── js/             # JavaScript files
│   └── images/         # Images and icons
├── templates/          # HTML templates
│   ├── index.html      # Main application UI
│   └── error.html      # Error page
└── instance/           # SQLite database (local only)
```

## 🏃‍♂️ Running Locally

### Prerequisites
- Python 3.8+ installed
- Git installed

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/LelahM/todoapp.git
   cd todoapp
   ```

2. **Run the simplified version** (recommended)
   ```bash
   python3 app_simple.py
   ```

3. **Or run the full version** (requires database setup)
   ```bash
   ./run.sh
   ```

4. **Open your browser**
   - Navigate to: [http://localhost:5001](http://localhost:5001)

## 📱 Screenshots & Features

### Main Dashboard
![GetTasked Dashboard](screenshots/gettasked-mockup.svg)
- Clean, modern interface with glassmorphism design
- Task overview with progress statistics
- Smart reminders section
- Quick task addition

### Task Management
- Intuitive task creation with categories and priorities
- Due date picker with time selection
- One-click task completion toggle
- Easy task deletion

### Analytics Dashboard
- Pie charts showing task distribution by category
- Completion rate visualization
- Progress tracking over time
- Motivational progress messages

## 🌐 Deployment Options

### 🎯 **Vercel (Recommended)**
1. Fork this repository
2. Connect to Vercel
3. Deploy automatically
4. **Live Demo**: [https://gettasked.vercel.app](https://gettasked.vercel.app)

### 🛠️ **Other Platforms**

#### Render.com
```bash
# Build Command
pip install -r requirements.txt

# Start Command  
python app_simple.py
```

#### Heroku
```bash
git push heroku main
```

#### Railway
```bash
railway login
railway link
railway up
```

## 🗂️ Project Structure

```
todoapp/
├── app_simple.py          # Simplified Flask app (serverless-ready)
├── app.py                 # Full Flask app with database
├── config.py              # Configuration settings
├── models.py              # Database models
├── index.py               # Vercel entry point
├── requirements.txt       # Python dependencies
├── vercel.json           # Vercel deployment config
├── README.md             # This file
├── templates/            # HTML templates
│   ├── index.html        # Main app interface
│   ├── error.html        # Error page
│   └── welcome.html      # Welcome page
└── static/               # Static assets
    └── js/
        └── app.js        # JavaScript functionality
```

## 🔧 Configuration

### Environment Variables
```bash
SECRET_KEY=your-secret-key-here
FLASK_ENV=development  # or production
```

### Local Development
- Uses file-based SQLite database
- Debug mode enabled
- Hot reload on file changes

### Production (Vercel)
- In-memory storage (resets on deployment)
- Optimized for serverless functions
- HTTPS enabled by default

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

## 🎯 Features in Development

- [ ] User authentication
- [ ] Data persistence across sessions
- [ ] Task sharing and collaboration
- [ ] Email reminders
- [ ] Dark/Light theme toggle
- [ ] Export functionality
- [ ] Mobile app (PWA)

## 🙋‍♂️ Support

- **Live Demo**: [https://gettasked.vercel.app](https://gettasked.vercel.app)
- **Issues**: [GitHub Issues](https://github.com/LelahM/todoapp/issues)
- **Repository**: [GitHub Repo](https://github.com/LelahM/todoapp)

## 👨‍💻 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 ToDo

- [ ] Add user authentication
- [ ] Add persistent database support (PostgreSQL)
- [ ] Implement task sharing functionality
- [ ] Add dark/light theme toggle
- [ ] Create mobile app version
- [ ] Replace mockup with actual app screenshot

> **Note:** To replace the mockup with an actual screenshot of your app:
> 1. Visit your app at [https://gettasked.vercel.app](https://gettasked.vercel.app)
> 2. Take a screenshot of the interface (Cmd+Shift+4 on macOS)
> 3. Save it as `screenshots/gettasked-dashboard.png`
> 4. Update the README.md image path to `screenshots/gettasked-dashboard.png`

---

**Made with ❤️ by [LelahM](https://github.com/LelahM)**

*GetTasked - Get organized, get productive, get things done!* ✨
