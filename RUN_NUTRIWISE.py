#!/usr/bin/env python3
"""
🥗 NutriWise v2.0 - One-Click Launcher
Run this file to start your modernized meal planner!
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import subprocess
import webbrowser
import time
from threading import Thread

def print_banner():
    print("=" * 60)
    print("🥗 NutriWise v2.0 - Modern AI Meal Planner")
    print("=" * 60)
    print("✨ Upgraded from Tkinter to Vue.js + FastAPI")
    print("🚀 Starting your modern web application...")
    print("=" * 60)

def start_backend():
    """Start the backend server"""
    print("🔧 Starting backend server...")
    backend_path = os.path.join(os.path.dirname(__file__), 'backend')
    demo_server_path = os.path.join(backend_path, 'demo_server.py')
    
    if os.path.exists(demo_server_path):
        os.chdir(backend_path)
        python_executable = sys.executable
        subprocess.run([python_executable, 'demo_server.py'])
    else:
        print("❌ Backend server not found!")

def start_frontend():
    """Start the frontend development server"""
    print("🎨 Starting frontend server...")
    frontend_path = os.path.join(os.path.dirname(__file__), 'frontend')
    
    if os.path.exists(frontend_path):
        os.chdir(frontend_path)
        
        # Check if node_modules exists
        if not os.path.exists('node_modules'):
            print("📦 Installing frontend dependencies...")
            subprocess.run(['npm', 'install'], check=True)
        
        print("🚀 Starting development server...")
        subprocess.run(['npm', 'run', 'dev'])
    else:
        print("❌ Frontend not found!")

def open_browser():
    """Open browser after a delay"""
    time.sleep(3)
    print("🌐 Opening browser...")
    webbrowser.open('http://localhost:3000')

def main():
    print_banner()
    
    choice = input("""
Choose how to run NutriWise v2.0:

1. 🚀 Full Stack (Backend + Frontend) - Recommended
2. 🔧 Backend Only (API server)
3. 🎨 Frontend Only (if backend is already running)
4. 📱 Open Browser (if servers are running)

Enter your choice (1-4): """).strip()

    if choice == '1':
        print("\n🚀 Starting Full Stack Application...")
        print("📝 Instructions:")
        print("   1. Backend will start first")
        print("   2. Open another terminal and run this script again")
        print("   3. Choose option 3 to start frontend")
        print("   4. Visit http://localhost:3000")
        
        # Start backend
        start_backend()
        
    elif choice == '2':
        print("\n🔧 Starting Backend Only...")
        start_backend()
        
    elif choice == '3':
        print("\n🎨 Starting Frontend Only...")
        # Open browser in background
        Thread(target=open_browser, daemon=True).start()
        start_frontend()
        
    elif choice == '4':
        print("\n🌐 Opening browser...")
        webbrowser.open('http://localhost:3000')
        
    else:
        print("❌ Invalid choice. Please run again and choose 1-4.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for using NutriWise v2.0!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Make sure you have Python and Node.js installed!")
