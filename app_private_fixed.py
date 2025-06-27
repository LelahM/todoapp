from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from datetime import datetime, timedelta
import os
import secrets
import uuid

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-for-demo-change-in-production')

# Simple user session-based storage
class SimpleTask:
    def __init__(self, title, category, priority, notes, due_date, task_id=None):
        self.id = task_id or str(uuid.uuid4())
        self.title = title
        self.category = category
        self.priority = priority
        self.notes = notes
        self.due_date = due_date
        self.completed = False
        self.created_at = datetime.utcnow()

def get_user_id():
    """Get or create a unique user ID for this session"""
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    return session['user_id']

def get_user_name():
    """Get user name from session or return default"""
    return session.get('user_name', 'Friend')

def set_user_name(name):
    """Set user name in session"""
    session['user_name'] = name

def get_user_tasks():
    """Get tasks for the current user session"""
    user_id = get_user_id()
    tasks_key = f'tasks_{user_id}'
    return session.get(tasks_key, [])

def save_user_tasks(tasks):
    """Save tasks for the current user session"""
    user_id = get_user_id()
    tasks_key = f'tasks_{user_id}'
    # Convert task objects to dictionaries for session storage
    tasks_data = []
    for task in tasks:
        tasks_data.append({
            'id': task.id,
            'title': task.title,
            'category': task.category,
            'priority': task.priority,
            'notes': task.notes,
            'due_date': task.due_date.isoformat() if task.due_date else None,
            'completed': task.completed,
            'created_at': task.created_at.isoformat()
        })
    session[tasks_key] = tasks_data

def tasks_from_session_data(tasks_data):
    """Convert session data back to task objects"""
    tasks = []
    for data in tasks_data:
        task = SimpleTask(
            title=data['title'],
            category=data['category'],
            priority=data['priority'],
            notes=data['notes'],
            due_date=datetime.fromisoformat(data['due_date']) if data['due_date'] else None,
            task_id=data['id']
        )
        task.completed = data['completed']
        task.created_at = datetime.fromisoformat(data['created_at'])
        tasks.append(task)
    return tasks

# Simple CSRF token function
def generate_csrf_token():
    return secrets.token_urlsafe(32)

# Make csrf_token available in templates
@app.context_processor
def inject_csrf_token():
    return dict(csrf_token=generate_csrf_token)

@app.route('/')
def index():
    try:
        # Get user-specific data
        user_name = get_user_name()
        tasks_data = get_user_tasks()
        tasks = tasks_from_session_data(tasks_data)
        
        complete_tasks = len([task for task in tasks if task.completed])
        total_tasks = len(tasks)
        
        now = datetime.utcnow()
        overdue_tasks = [task for task in tasks if not task.completed and task.due_date and task.due_date < now]
        
        today_start = datetime(now.year, now.month, now.day)
        today_end = today_start + timedelta(days=1)
        due_today_tasks = [task for task in tasks if not task.completed and task.due_date and today_start <= task.due_date < today_end]
        
        soon = now + timedelta(hours=24)
        due_soon_tasks = [task for task in tasks if not task.completed and task.due_date and now <= task.due_date <= soon]
        
        week_end = now + timedelta(days=7)
        due_this_week_tasks = [task for task in tasks if not task.completed and task.due_date and soon < task.due_date <= week_end]
        
        motivation = get_motivation_message(complete_tasks/total_tasks if total_tasks > 0 else 0, user_name)
        
        # Create a simple user object for template
        user = type('User', (), {'name': user_name, 'id': get_user_id()})()
        
        return render_template('index_private.html',
                             user=user,
                             tasks=tasks,
                             complete_tasks=complete_tasks,
                             total_tasks=total_tasks,
                             overdue_tasks=overdue_tasks,
                             due_today_tasks=due_today_tasks,
                             due_soon_tasks=due_soon_tasks,
                             due_this_week_tasks=due_this_week_tasks,
                             motivation=motivation,
                             reminder="Your data is private to your session",
                             datetime=datetime)
    except Exception as e:
        print(f"Error in index route: {e}")
        return f"<h1>GetTasked - Private Mode</h1><p>Error: {str(e)}</p><p>Your data is private to your session.</p>"

@app.route('/add_task', methods=['POST'])
def add_task():
    try:
        title = request.form.get('title')
        category = request.form.get('category')
        priority = request.form.get('priority')
        notes = request.form.get('notes')
        due_date_str = request.form.get('due_date')
        due_date = datetime.strptime(due_date_str, '%Y-%m-%dT%H:%M') if due_date_str else None
        
        # Get current user's tasks
        tasks_data = get_user_tasks()
        tasks = tasks_from_session_data(tasks_data)
        
        # Create new task
        task = SimpleTask(title=title,
                         category=category,
                         priority=priority,
                         notes=notes,
                         due_date=due_date)
        
        tasks.append(task)
        save_user_tasks(tasks)
        
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error adding task: {e}")
        return redirect(url_for('index'))

@app.route('/toggle_task/<task_id>', methods=['POST'])
def toggle_task(task_id):
    try:
        # Get current user's tasks
        tasks_data = get_user_tasks()
        tasks = tasks_from_session_data(tasks_data)
        
        # Find and toggle the task
        task = next((t for t in tasks if t.id == task_id), None)
        if task:
            task.completed = not task.completed
            save_user_tasks(tasks)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'completed': task.completed if task else False})
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error toggling task: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/delete_task/<task_id>', methods=['POST'])
def delete_task(task_id):
    try:
        # Get current user's tasks
        tasks_data = get_user_tasks()
        tasks = tasks_from_session_data(tasks_data)
        
        # Remove the task
        tasks = [t for t in tasks if t.id != task_id]
        save_user_tasks(tasks)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True})
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error deleting task: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/update_name', methods=['POST'])
def update_name():
    try:
        name = request.form.get('name')
        set_user_name(name)
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error updating name: {e}")
        return redirect(url_for('index'))

@app.route('/get_stats')
def get_stats():
    try:
        # Get current user's tasks
        tasks_data = get_user_tasks()
        tasks = tasks_from_session_data(tasks_data)
        
        categories = {}
        completed_by_category = {}
        
        for task in tasks:
            if task.category not in categories:
                categories[task.category] = 0
                completed_by_category[task.category] = 0
            categories[task.category] += 1
            if task.completed:
                completed_by_category[task.category] += 1
        
        completion = {
            'Completed': len([t for t in tasks if t.completed]),
            'Remaining': len([t for t in tasks if not t.completed])
        }
        
        return jsonify({
            'categories': categories,
            'completed_by_category': completed_by_category,
            'completion': completion
        })
    except Exception as e:
        print(f"Error getting stats: {e}")
        return jsonify({'error': str(e)})

@app.route('/clear_session', methods=['POST'])
def clear_session():
    """Clear current user's session data"""
    try:
        user_id = get_user_id()
        tasks_key = f'tasks_{user_id}'
        session.pop(tasks_key, None)
        session.pop('user_name', None)
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error clearing session: {e}")
        return redirect(url_for('index'))

def get_motivation_message(completion_rate, user_name):
    if completion_rate >= 0.8:
        return f"Amazing work, {user_name}! You're crushing your goals! 🌟"
    elif completion_rate >= 0.5:
        return f"You're making great progress, {user_name}! Keep up the momentum! 💪"
    elif completion_rate >= 0.3:
        return f"You've got this, {user_name}! Every completed task counts! 🎯"
    else:
        return f"Ready to make today amazing, {user_name}? Start with one task! ⭐"

if __name__ == '__main__':
    app.run(debug=True, port=5002)
