#!/bin/bash
# AI Appointment Assistant - Quick Setup Script
# Run this after cloning the repository

echo "🤖 AI Appointment Assistant - Setup Script"
echo "=========================================="

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python found: $(python --version)"

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed. Please install pip first."
    exit 1
fi

echo "✅ pip found"

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Copy environment template
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your actual API keys."
else
    echo "ℹ️  .env file already exists."
fi

# Create credentials directory
mkdir -p config/credentials

echo ""
echo "🚀 Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Groq API key"
echo "2. Add your Google service account JSON to config/credentials/service_account.json"
echo "3. Run: streamlit run streamlit_app.py"
echo ""
echo "For detailed instructions, see README.md"
