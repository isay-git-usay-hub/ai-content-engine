#!/usr/bin/env python3
"""Environment setup script for AI Content Strategy Engine"""

import os
import sys
from pathlib import Path

def create_env_file():
    """Create .env file from template"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return
    
    if env_example.exists():
        # Copy template and ask for API key
        with open(env_example) as f:
            content = f.read()
        
        # Prompt for Groq API key
        api_key = input("Enter your Groq API key: ").strip()
        if api_key:
            content = content.replace("your_groq_api_key_here", api_key)
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ .env file created successfully")
    else:
        print("❌ .env.example file not found")

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_requirements():
    """Install Python requirements"""
    import subprocess
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        sys.exit(1)

if __name__ == "__main__":
    print("🚀 Setting up AI Content Strategy Engine...")
    check_python_version()
    create_env_file()
    install_requirements()
    print("🎉 Setup completed! Run 'python scripts/run_server.py' to start the server.")
