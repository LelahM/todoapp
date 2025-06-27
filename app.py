from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime, timedelta
from config import Config, DevelopmentConfig
from models import db, User, Task
from flask_wtf.csrf import CSRFProtect
import os

def create_app(config_class=None):
    app = Flask(__name__)
    
    # Choose config based on environment
    if config_class is None:
        if os.environ.get('FLASK_ENV') == 'development':
            config_class = DevelopmentConfig
        else:
            config_class = Config
    
    app.config.from_object(config_class)
    
    # Print database URI for debugging
    print(f"Using database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    # Ensure instance folder exists (only for local development)
    if app.config.get('DEBUG'):
        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass
    
    # Initialize extensions
    db.init_app(app)
    csrf = CSRFProtect(app)
    
    # Initialize database
    def init_db():
        """Initialize database tables and default data"""
        try:
            db.create_all()
            # Create default user if none exists
            if not User.query.first():
                default_user = User(name="Friend")
                db.session.add(default_user)
                db.session.commit()
            print("Database initialized successfully")
        except Exception as e:
            print(f"Database initialization error: {e}")
    
    @app.before_request
    def ensure_db():
        """Ensure database is initialized for each request in serverless environment"""
        # Always try to initialize database for serverless/production environments
        if (os.environ.get('VERCEL') or 
            os.environ.get('VERCEL_ENV') or 
            os.environ.get('FLASK_ENV') == 'production'):
            try:
                # Try to query users table to see if it exists
                User.query.first()
            except Exception:
                # Tables don't exist, initialize them
                with app.app_context():
                    init_db()
    
    # Create database tables for local development
    if not (os.environ.get('VERCEL') or 
            os.environ.get('VERCEL_ENV') or 
            os.environ.get('FLASK_ENV') == 'production'):
        with app.app_context():
            init_db()
    
    @app.route('/')
    def index():
        try:
            user = User.query.first()
            tasks = Task.query.all()
            complete_tasks = len([task for task in tasks if task.completed])
            total_tasks = len(tasks)
            
            now = datetime.utcnow()
            overdue_tasks = Task.query.filter(Task.completed == False, 
                                            Task.due_date < now).all()
            
            today_start = datetime(now.year, now.month, now.day)
            today_end = today_start + timedelta(days=1)
            due_today_tasks = Task.query.filter(Task.completed == False,
                                              Task.due_date >= today_start,
                                              Task.due_date < today_end).all()
            
            soon = now + timedelta(hours=24)
            due_soon_tasks = Task.query.filter(Task.completed == False,
                                             Task.due_date <= soon,
                                             Task.due_date >= now).all()
            
            week_end = now + timedelta(days=7)
            due_this_week_tasks = Task.query.filter(Task.completed == False,
                                                  Task.due_date > soon,
                                                  Task.due_date <= week_end).all()
            
            motivation = get_motivation_message(complete_tasks/total_tasks if total_tasks > 0 else 0, user.name)
            reminder = ""
            
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
                                 reminder=reminder,
                                 datetime=datetime)
        except Exception as e:
            print(f"Error in index route: {e}")
            return render_template('error.html', error=str(e))
    
    @app.route('/add_task', methods=['POST'])
    def add_task():
        title = request.form.get('title')
        category = request.form.get('category')
        priority = request.form.get('priority')
        notes = request.form.get('notes')
        due_date = datetime.strptime(request.form.get('due_date'), '%Y-%m-%dT%H:%M')
        
        task = Task(title=title,
                   category=category,
                   priority=priority,
                   notes=notes,
                   due_date=due_date,
                   user_id=User.query.first().id)
        
        db.session.add(task)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    @app.route('/toggle_task/<int:task_id>', methods=['POST'])
    def toggle_task(task_id):
        task = Task.query.get_or_404(task_id)
        task.completed = not task.completed
        db.session.commit()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'completed': task.completed})
        return redirect(url_for('index'))
    
    @app.route('/delete_task/<int:task_id>', methods=['POST'])
    def delete_task(task_id):
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True})
        return redirect(url_for('index'))
    
    @app.route('/update_name', methods=['POST'])
    def update_name():
        name = request.form.get('name')
        user = User.query.first()
        user.name = name
        db.session.commit()
        return redirect(url_for('index'))
    
    @app.route('/get_stats')
    def get_stats():
        tasks = Task.query.all()
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
    
    return app

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
    app = create_app()
    print("GetTasked - © 2025 Le'lah Mckoy. All Rights Reserved.")
    app.run(debug=True, port=5001)
