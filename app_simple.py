from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime, timedelta
import os
import secrets

# Simple in-memory storage for Vercel serverless
class SimpleUser:
    def __init__(self, name="Friend"):
        self.name = name
        self.id = 1

class SimpleTask:
    def __init__(self, title, category, priority, notes, due_date, user_id=1):
        self.id = len(tasks) + 1
        self.title = title
        self.category = category
        self.priority = priority
        self.notes = notes
        self.due_date = due_date
        self.user_id = user_id
        self.completed = False
        self.created_at = datetime.utcnow()

# Global storage (resets with each serverless function call)
user = SimpleUser()
tasks = []

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-for-demo')

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
        complete_tasks = len([task for task in tasks if task.completed])
        total_tasks = len(tasks)
        
        now = datetime.utcnow()
        overdue_tasks = [task for task in tasks if not task.completed and task.due_date < now]
        
        today_start = datetime(now.year, now.month, now.day)
        today_end = today_start + timedelta(days=1)
        due_today_tasks = [task for task in tasks if not task.completed and today_start <= task.due_date < today_end]
        
        soon = now + timedelta(hours=24)
        due_soon_tasks = [task for task in tasks if not task.completed and now <= task.due_date <= soon]
        
        week_end = now + timedelta(days=7)
        due_this_week_tasks = [task for task in tasks if not task.completed and soon < task.due_date <= week_end]
        
        motivation = get_motivation_message(complete_tasks/total_tasks if total_tasks > 0 else 0, user.name)
        
        return render_template('index.html',
                             user=user,
                             tasks=tasks,
                             complete_tasks=complete_tasks,
                             total_tasks=total_tasks,
                             overdue_tasks=overdue_tasks,
                             due_today_tasks=due_today_tasks,
                             due_soon_tasks=due_soon_tasks,
                             due_this_week_tasks=due_this_week_tasks,
                             motivation=motivation,
                             reminder="",
                             datetime=datetime)
    except Exception as e:
        print(f"Error in index route: {e}")
        return f"<h1>GetTasked - Demo Mode</h1><p>Error: {str(e)}</p><p>This is a serverless demo. Data resets with each visit.</p>"

@app.route('/add_task', methods=['POST'])
def add_task():
    try:
        title = request.form.get('title')
        category = request.form.get('category')
        priority = request.form.get('priority')
        notes = request.form.get('notes')
        due_date = datetime.strptime(request.form.get('due_date'), '%Y-%m-%dT%H:%M')
        
        task = SimpleTask(title=title,
                         category=category,
                         priority=priority,
                         notes=notes,
                         due_date=due_date)
        
        tasks.append(task)
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error adding task: {e}")
        return redirect(url_for('index'))

@app.route('/toggle_task/<int:task_id>', methods=['POST'])
def toggle_task(task_id):
    try:
        task = next((t for t in tasks if t.id == task_id), None)
        if task:
            task.completed = not task.completed
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'completed': task.completed if task else False})
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error toggling task: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    try:
        global tasks
        tasks = [t for t in tasks if t.id != task_id]
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True})
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error deleting task: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/update_name', methods=['POST'])
def update_name():
    try:
        global user
        name = request.form.get('name')
        user.name = name
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error updating name: {e}")
        return redirect(url_for('index'))

@app.route('/get_stats')
def get_stats():
    try:
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
    app.run(debug=True, port=5001)
