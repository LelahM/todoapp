from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from datetime import datetime, timedelta
import os
import secrets
import uuid
import json
from werkzeug.security import generate_password_hash

app = Flask(__name__)
# Use a more secure secret key generation method
app.secret_key = os.environ.get('SECRET_KEY', generate_password_hash(secrets.token_hex(32)))
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)  # Set session to last for 31 days
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('PRODUCTION') == '1'  # Secure cookies in production
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript from accessing cookies
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
app.config['SESSION_TYPE'] = 'filesystem'  # More reliable than signed cookies
app.config['SESSION_USE_SIGNER'] = True    # Add cryptographic signing to cookie session ID

# Additional privacy and security headers
@app.after_request
def add_security_headers(response):
    """Add security headers for enhanced privacy"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    # Don't cache sensitive pages
    if request.endpoint in ['index', 'get_stats']:
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    return response

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
        session.permanent = True  # Ensure this specific session is permanent
        session['user_id'] = str(uuid.uuid4())
    return session['user_id']

def get_user_name():
    """Get user name from session or return default"""
    return session.get('user_name', 'Friend')

def set_user_name(name):
    """Set user name in session"""
    session['user_name'] = name
    # Make sure the session is saved immediately
    session.modified = True

def get_user_tasks():
    """Get tasks for the current user session"""
    try:
        user_id = get_user_id()
        tasks_key = f'tasks_{user_id}'
        tasks_data = session.get(tasks_key, [])
        
        # Privacy logging - ensure isolation
        print(f"Privacy Check: User {user_id[:8]}... accessing {len(tasks_data)} tasks")
        
        return tasks_from_session_data(tasks_data)
    except Exception as e:
        print(f"Error retrieving tasks: {e}")
        return []

def save_user_tasks(tasks):
    """Save tasks for the current user session"""
    user_id = get_user_id()
    tasks_key = f'tasks_{user_id}'
    
    # Privacy logging - ensure isolation
    print(f"Privacy Check: User {user_id[:8]}... saving {len(tasks)} tasks to isolated session")
    
    # Convert task objects to dictionaries for session storage
    tasks_data = []
    for task in tasks:
        # Create a serializable dict with minimal data to fit in cookie size limits
        task_dict = {
            'id': task.id,
            'title': task.title[:100] if task.title else "",  # Limit title length
            'category': task.category[:20] if task.category else "", 
            'priority': task.priority[:10] if task.priority else "",
            'notes': task.notes[:200] if task.notes else "",  # Limit notes length
            'due_date': task.due_date.isoformat() if task.due_date else None,
            'completed': task.completed,
            'created_at': task.created_at.isoformat() if task.created_at else datetime.utcnow().isoformat()
        }
        tasks_data.append(task_dict)
    
    # Ensure we're not exceeding cookie size limits (typically ~4KB)
    # If too many tasks, keep only the most recent ones
    if len(str(tasks_data)) > 3500:  # Leave some margin for other session data
        tasks_data = tasks_data[-20:]  # Keep only the 20 most recent tasks
    
    session[tasks_key] = tasks_data

def tasks_from_session_data(tasks_data):
    """Convert session data back to task objects"""
    tasks = []
    if not tasks_data:
        return tasks
    
    for data in tasks_data:
        try:
            # Handle potentially missing or malformed data
            title = data.get('title', '')
            category = data.get('category', '')
            priority = data.get('priority', 'medium')
            notes = data.get('notes', '')
            due_date = None
            if data.get('due_date'):
                try:
                    due_date = datetime.fromisoformat(data['due_date'])
                except (ValueError, TypeError):
                    due_date = None
            
            task = SimpleTask(
                title=title,
                category=category,
                priority=priority,
                notes=notes,
                due_date=due_date,
                task_id=data.get('id', str(uuid.uuid4()))
            )
            task.completed = bool(data.get('completed', False))
            
            # Handle created_at date
            try:
                if data.get('created_at'):
                    task.created_at = datetime.fromisoformat(data['created_at'])
                else:
                    task.created_at = datetime.utcnow()
            except (ValueError, TypeError):
                task.created_at = datetime.utcnow()
                
            tasks.append(task)
        except Exception as e:
            # Skip invalid task data
            print(f"Error parsing task data: {e}")
            continue
            
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
        print("Index route called")
        # Get user-specific data
        user_name = get_user_name()
        print(f"User name: {user_name}")
        tasks = get_user_tasks()  # Now returns Task objects directly
        print(f"Number of tasks: {len(tasks)}")
        
        # Set up session permanence on each request
        session.permanent = True
        
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
        
        # Check for name update notifications
        name_updated = session.pop('name_updated', False)
        name_error = session.pop('name_error', False)
        
        print("About to render template")
        result = render_template('index_private_simple.html',
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
                             name_updated=name_updated,
                             name_error=name_error,
                             datetime=datetime)
        print(f"Template rendered, length: {len(result)}")
        return result
    except Exception as e:
        print(f"Error in index route: {e}")
        import traceback
        traceback.print_exc()
        return f"<h1>GetTasked - Private Mode</h1><p>Error: {str(e)}</p><p>Your data is private to your session.</p>"

@app.route('/add_task', methods=['POST'])
def add_task():
    try:
        title = request.form.get('task')  # Changed from 'title' to 'task' to match form field
        category = request.form.get('category')
        priority = request.form.get('priority')
        notes = request.form.get('notes')
        due_date_str = request.form.get('due_date')
        due_date = None
        if due_date_str:
            try:
                # Try datetime format first (from datetime-local input)
                due_date = datetime.strptime(due_date_str, '%Y-%m-%dT%H:%M')
            except ValueError:
                try:
                    # Fallback to date format (from date input)
                    due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
                except ValueError:
                    # If both fail, set to None
                    due_date = None
        
        # Get current user's tasks (this already returns processed task objects)
        tasks = get_user_tasks()
        
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
        # Get current user's tasks (this already returns processed task objects)
        tasks = get_user_tasks()
        
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
        # Get current user's tasks (this already returns processed task objects)
        tasks = get_user_tasks()
        
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
        if name:
            print(f"Setting user name to: {name}")
            set_user_name(name)
            # Store a success message in session flash
            session['name_updated'] = True
        else:
            print("No name provided in form")
            session['name_error'] = True
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error updating name: {e}")
        session['name_error'] = True
        return redirect(url_for('index'))

@app.route('/get_stats')
def get_stats():
    try:
        # Get current user's tasks (this already returns processed task objects)
        tasks = get_user_tasks()
        
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
