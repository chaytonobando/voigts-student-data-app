#!/bin/bash

# 🚀 GitHub Repository Setup Script for Voigts Student Data Processing Suite
# This script will help you create and push to a new GitHub repository

echo "🚌 Voigts Student Data Processing Suite - Repository Setup"
echo "========================================================="
echo ""

# Repository details
REPO_NAME="voigts-student-data-app"
REPO_DESCRIPTION="Professional student transportation data processing suite with AI-powered PDF extraction and data validation"

echo "📋 Repository Details:"
echo "   Name: $REPO_NAME"
echo "   Description: $REPO_DESCRIPTION"
echo ""

echo "🔧 Manual Setup Instructions:"
echo ""
echo "1. CREATE GITHUB REPOSITORY:"
echo "   → Go to: https://github.com/new"
echo "   → Repository name: $REPO_NAME"
echo "   → Description: $REPO_DESCRIPTION"
echo "   → Make it PUBLIC (required for free Streamlit Cloud)"
echo "   → DO NOT initialize with README, .gitignore, or license"
echo "   → Click 'Create repository'"
echo ""

echo "2. COPY AND RUN THESE COMMANDS:"
echo "   (Replace YOUR_USERNAME with your actual GitHub username)"
echo ""
echo "   git remote add origin https://github.com/YOUR_USERNAME/$REPO_NAME.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""

echo "3. VERIFY REPOSITORY:"
echo "   → Check that all files are uploaded:"
echo "     - streamlit_app.py"
echo "     - requirements.txt"
echo "     - README.md"
echo "     - DEPLOYMENT_GUIDE.md"
echo "     - Voigts Bus Service Logo.png"
echo "     - .streamlit/secrets.toml (should be ignored by git)"
echo ""

echo "4. DEPLOY TO STREAMLIT CLOUD:"
echo "   → Go to: https://share.streamlit.io"
echo "   → Click 'New app'"
echo "   → Repository: YOUR_USERNAME/$REPO_NAME"
echo "   → Branch: main"
echo "   → Main file: streamlit_app.py"
echo "   → Click 'Deploy!'"
echo ""

echo "5. ADD SECRETS IN STREAMLIT CLOUD:"
echo "   → In app settings → Secrets → Add these:"
echo ""
echo "   [azure]"
echo "   endpoint = \"https://rocoristudents.cognitiveservices.azure.com/\""
echo "   api_key = \"CeONvzJqeNhNBVaEJQW42seJ1UwOYdCebflbbdrGdRMMW5k30aeWJQQJ99BGACYeBjFXJ3w3AAALACOGjt98\""
echo ""
echo "   [app]"
echo "   title = \"Voigts Student Opt-In Data Management Suite\""
echo "   description = \"Professional transportation data processing for school districts\""
echo ""

echo "🎉 That's it! Your app will be live and ready to use!"
echo ""
echo "📱 Expected URL: https://YOUR_USERNAME-voigts-student-data-app.streamlit.app"
echo ""

# Check current directory contents
echo "📁 Current Repository Contents:"
ls -la | grep -v "^total\|^d.*\.$" | head -10
echo ""

echo "✅ Ready for GitHub upload!"
