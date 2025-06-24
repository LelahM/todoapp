#!/bin/bash

# Vercel Deployment Script for GetTasked Todo App
echo "🚀 Deploying GetTasked to Vercel..."

# Check if git is clean
if [ -n "$(git status --porcelain)" ]; then
    echo "❌ Git working directory is not clean. Please commit your changes first."
    exit 1
fi

echo "✅ Git is clean, ready for deployment"

# Push to GitHub to trigger Vercel deployment
echo "📤 Pushing to GitHub..."
git push origin main

echo "🎉 Code pushed to GitHub!"
echo ""
echo "🌐 To complete deployment:"
echo "1. Go to https://vercel.com"
echo "2. Click 'New Project'"
echo "3. Import from GitHub: https://github.com/LelahM/todoapp"
echo "4. Deploy with default settings"
echo ""
echo "📋 Or use this one-click deploy:"
echo "👉 https://vercel.com/new/clone?repository-url=https://github.com/LelahM/todoapp"
