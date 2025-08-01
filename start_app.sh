#!/bin/bash

echo "🚀 Vendor Evaluation Tool - Quick Start"
echo "======================================"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found"
    echo ""
    echo "📋 Please create a .env file with your AWS credentials first:"
    echo ""
    echo "Create a .env file in the project directory with these contents:"
    echo "AWS_ACCESS_KEY_ID=your_access_key_here"
    echo "AWS_SECRET_ACCESS_KEY=your_secret_key_here"
    echo "AWS_SESSION_TOKEN=your_session_token_here"
    echo "AWS_DEFAULT_REGION=us-west-2"
    echo ""
    echo "Or run the setup script: python setup_credentials.py"
    echo ""
    echo "Then run this script again: ./start_app.sh"
    exit 1
fi

echo "✅ .env file found"
echo ""

# Test the setup
echo "🔍 Testing setup..."
python test_setup.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Setup verified! Starting the application..."
    echo "📱 Open your browser and go to: http://localhost:8501"
    echo ""
    echo "Press Ctrl+C to stop the application when done."
    echo ""
    
    # Start the application
    streamlit run main.py --server.port 8501
else
    echo ""
    echo "❌ Setup test failed. Please check your .env file and try again."
    exit 1
fi 