from app_private import app

# Vercel entry point - uses session-based private storage
# Each user gets their own private data stored in Flask sessions
# Data is isolated per user session and not visible to others

if __name__ == "__main__":
    app.run()
