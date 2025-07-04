# GetTasked - Private Task Management Application

A beautiful, feature-rich task management application built with Flask, featuring a stunning glassmorphism UI design and **private user sessions** that keep your data secure and hidden from other users.

## 🔒 Privacy & Security

- **🔐 Individual Sessions**: Each user gets a unique, private session
- **👤 Data Isolation**: Your tasks are only visible to you
- **🚫 No Shared Data**: Tasks from other users are completely hidden
- **💾 Session Storage**: Data is stored securely in your browser session
- **🗑️ Data Control**: Clear your data anytime with one click
- **♻️ Persistent Data**: Your tasks remain available even after closing the browser
- **⏳ Long-Lasting**: Sessions persist for 31 days without losing your data
- **🔐 Enhanced Security**: Cryptographic signing for session cookies and improved security measures

## 🌐 Live Demo

**🚀 [Try GetTasked Live on Vercel](https://gettasked.vercel.app)**

Experience the full-featured todo application with real-time task management, progress tracking, and beautiful visualizations.

## ✅ Recent Fixes (June 28, 2025)

**Critical Issues Resolved:**
1. **Name Editing Functionality** - Fixed form field mismatch and corrupted JavaScript - ✅ Working
2. **Charts Display** - Restored Chart.js integration and fixed template corruption - ✅ Working  
3. **Date Parsing** - Enhanced to support both date and datetime formats - ✅ Working
4. **Session Persistence** - Improved reliability for long-running sessions - ✅ Working

**Technical Details:**
- Fixed Flask route form field name (`'title'` → `'task'`)
- Restored Chart.js CDN and chart creation code
- Added completion chart (doughnut) and category chart (bar)
- Enhanced error handling for date input formats
- Improved session security with cryptographic signing

**Verification:**
- ✅ Name editing: User can update display name successfully
- ✅ Task management: Add, complete, and delete tasks working
- ✅ Charts: Visual analytics displaying completion and category data
- ✅ Data persistence: Sessions maintain data across browser sessions

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

### 👤 **Privacy & Personalization**
- 🔒 **Private Sessions**: Your data is completely isolated from other users
- 🏷️ **Custom Username**: Personalized experience for each session
- 🎨 **Theme Consistency**: Beautiful color coordination
- 💾 **Secure Storage**: Session-based data storage
- 🗑️ **Data Control**: Clear your personal data anytime

## 🔄 New Features (June 2025)

- **📊 Task Filtering & Sorting**: Sort tasks by due date, creation date, or priority, and filter by category, status, and more
- **📈 Enhanced Statistics**: Detailed visualizations of your task data with beautiful charts
- **🎨 Visual Task Indicators**: Clearer visual indicators for task priorities and deadlines
- **♿ Accessibility Improvements**: ARIA attributes, keyboard navigation support, and improved color contrast
- **📱 Responsive Design**: Better responsive design for all screen sizes
- **🔔 Task Reminders**: Quick view of overdue, due today, and upcoming tasks
- **🔍 Search & Filter**: Find tasks quickly with powerful search and filter options

## ✅ Fixed Issues (June 27, 2025)

### Issues Resolved:
1. **✅ Name Editing Fixed**: 
   - Fixed the `toggleNameEdit()` JavaScript function
   - Corrected form field name from `'title'` to `'task'` in add_task route
   - Added proper success/error feedback messages
   - Name editing now works seamlessly

2. **✅ Charts Now Working**: 
   - Fixed JavaScript syntax errors in template
   - Properly structured Chart.js initialization
   - Charts only display when there are tasks to visualize
   - Both completion chart (doughnut) and category chart (bar) now render correctly

3. **✅ Template Cleanup**:
   - Removed corrupted JavaScript code
   - Created clean, working HTML template
   - Improved accessibility with ARIA attributes
   - Added proper error handling for all AJAX requests

### Technical Fixes Made:
- **Backend**: Fixed parameter mismatch in Flask routes (title → task)
- **Frontend**: Rebuilt JavaScript with proper syntax and error handling
- **UI/UX**: Added visual feedback for name updates and better task organization
- **Charts**: Implemented Chart.js with proper data fetching and rendering

## 🚀 Quick Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/LelahM/todoapp)

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Charts**: Chart.js
- **Styling**: Custom CSS with Glassmorphism
- **Icons**: Unicode Emojis
- **Deployment**: Vercel (Serverless)
- **Storage**: Flask-Session with filesystem persistence
- **Privacy**: Individual user sessions with data isolation
- **Persistence**: 31-day session lifetime with secure storage

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
![GetTasked Dashboard](https://raw.githubusercontent.com/LelahM/todoapp/main/screenshots/Picture.png)
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

This app is optimized for serverless deployment on Vercel. Here's how to deploy your own instance:

1. **Fork this repository** to your GitHub account
2. **Import project to Vercel**:
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "New Project" 
   - Import your GitHub repository
   - Select the "todoapp" repository
3. **Configure deployment settings**:
   - Framework Preset: Other
   - Build Command: `pip install -r requirements_simple.txt`
   - Output Directory: Leave empty
   - Install Command: Leave default
4. **Add environment variables** (optional):
   - `SECRET_KEY`: Generate a random string for security
5. **Deploy!** Click "Deploy" and wait for the build to complete
6. **Visit your deployed app** at the URL provided by Vercel (e.g., `https://your-app-name.vercel.app`)

👉 **Live Demo**: [https://gettasked.vercel.app](https://gettasked.vercel.app)

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

## 🚀 Understanding Vercel Deployment

GetTasked is optimized for Vercel's serverless environment with privacy-focused adaptations:

### Privacy & Security Features
- **Session-Based Storage**: Each user gets a unique session with isolated data
- **Private Sessions**: Your tasks are never visible to other users
- **Secure Entry Point**: `app_private.py` ensures data isolation
- **No Shared State**: Each user session is completely independent

### Serverless Optimizations
- **Private Version**: `app_private.py` uses secure session storage
- **Vercel Entry Point**: `index.py` serves as the main entry point for Vercel
- **Reduced Dependencies**: Optimized for serverless deployment

### How It Works
1. When you visit the app, Vercel creates a secure session just for you
2. Your tasks are stored in your private session and never shared
3. Other users cannot see your data, even on the same deployment
4. You can clear your personal data anytime using the "Clear My Data" button
5. Static files (CSS, JS, images) are served directly by Vercel's CDN

### vercel.json Configuration
```json
{
  "version": 2,
  "builds": [{ 
    "src": "./index.py", 
    "use": "@vercel/python" 
  }],
  "routes": [{ 
    "src": "/(.*)", 
    "dest": "/index.py" 
  }]
}
```

### Privacy Notes
- **Session Storage**: Your data is stored securely in your browser session
- **Data Isolation**: Complete separation between different users
- **No Persistence**: Data is automatically cleared when your session ends
- **User Control**: You can manually clear your data anytime
- Static assets in the `static` folder are automatically served

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

## 📸 Adding Your Own Screenshots

To add your own screenshot of the live app to the README:

1. **Take a screenshot** of your deployed app:
   - Visit your app at [https://gettasked.vercel.app](https://gettasked.vercel.app)
   - Take a screenshot (Cmd+Shift+4 on macOS, Win+Shift+S on Windows)
   
2. **Save the screenshot** to your repository:
   - Name it something like `gettasked-live.png`
   - Add it to the `screenshots` folder in your repository:
   ```bash
   # Run in your project directory
   mv ~/Downloads/your-screenshot.png ./screenshots/gettasked-live.png
   ```

3. **Commit and push** the screenshot to GitHub:
   ```bash
   git add screenshots/gettasked-live.png
   git commit -m "Add live app screenshot"
   git push origin main
   ```

4. **Update the README.md** with the correct GitHub raw URL:
   - Change the image path in README.md to:
   ```
   ![GetTasked Dashboard](https://raw.githubusercontent.com/LelahM/todoapp/main/screenshots/gettasked-live.png)
   ```

> **Important:** Always use the full GitHub raw URL format (`https://raw.githubusercontent.com/username/repo/branch/path`) for images in your README to ensure they display properly on both GitHub and other platforms.

---

**Made with ❤️ by [Le'lah Mckoy](https://github.com/LelahM)**

© 2025 Le'lah Mckoy. All rights reserved.

*GetTasked - Get organized, get productive, get things done!* ✨
