from app_simple import app

# Vercel entry point - uses simplified in-memory storage
# No database dependencies, perfect for serverless

if __name__ == "__main__":
    app.run()
