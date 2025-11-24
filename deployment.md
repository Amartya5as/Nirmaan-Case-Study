# Deployment Guide

## Render Deployment
1. Create new Web Service
2. Connect GitHub repo
3. Use:
   - Build: pip install -r requirements.txt
   - Start: python backend/flask_app.py
4. Expose port via Render environment

## Railway Deployment
1. Create new service → Python
2. Add repo
3. Start command:
   python backend/flask_app.py

## AWS EC2 Deployment
1. Launch EC2 free tier instance
2. Install Python + Git
3. Clone repo
4. Run:
   python backend/flask_app.py
5. Reverse proxy with Nginx for production
