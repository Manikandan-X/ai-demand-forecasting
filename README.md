# AI Demand Forecasting System

An advanced AI-powered full-stack demand forecasting platform that predicts future product demand using historical sales datasets and provides real-time analytics, forecasting insights, notifications, reporting, and admin management features.

---

# Project Overview

This system helps businesses analyze historical sales data, generate future demand forecasts using Machine Learning models, monitor forecasting performance, and visualize analytics through an interactive dashboard.

The platform includes:

- AI-based forecasting
- Advanced analytics dashboard
- Admin management system
- Real-time notifications
- Report generation
- Forecast history tracking
- Docker deployment support
- Responsive frontend UI

---

# Features

# Authentication Module

- User Registration
- User Login
- JWT Authentication
- Protected APIs
- Session Handling
- Role-Based Access Control
- Admin/User Authorization

---

# Dataset Upload Module

- Upload CSV/Excel datasets
- Dataset validation
- Missing value handling
- Duplicate record removal
- Database dataset storage
- Upload failure notifications

---

# AI Forecasting Module

- Data preprocessing using Pandas
- Forecast generation using:
  - Linear Regression
  - Prophet Forecasting
- Multiple model support
- Forecast model comparison
- Forecast accuracy tracking
- Forecast history management
- Prediction analytics storage

---

# Dashboard & Analytics

- Total Sales Analytics
- Total Orders Analytics
- Monthly Sales Trends
- Forecast Accuracy Metrics
- Top Products Analysis
- Product Category Filtering
- Region Filtering
- Date Range Filtering
- Recent Forecast Activities
- Interactive Charts & Graphs
- Advanced Analytics Visualization

---

# Notifications Module

- In-app notifications
- Forecast completion notifications
- Report generation notifications
- Dataset upload failure alerts
- Notification dropdown system
- Mark all notifications as read

---

# Admin Panel Module

- Admin Dashboard
- User Management
- Dataset Management
- Forecast Monitoring
- Reports Monitoring
- System Analytics Overview

---

# Reports Module

- Detailed Forecast Reports
- Excel Report Export
- PDF Report Export
- Analytics Summary Reports
- Improved Report Formatting
- Downloadable Reports

---

# Frontend Enhancements

- Responsive UI Design
- Mobile-Friendly Layout
- Sidebar Navigation
- Loading Animations
- Skeleton Screens
- Reusable Components
- Improved UI/UX
- Forecast Visualization

---

# Performance Optimization

- Query Optimization
- Async APIs
- Database Indexing
- Connection Pooling
- Pagination Support
- Advanced API Validation
- Search & Filter APIs

---

# Production Features

- Docker Support
- WebSocket Notifications
- Background Tasks
- Production-Ready API Structure
- Optimized Database Performance

---

# Tech Stack

# Backend

- FastAPI
- MySQL
- SQLAlchemy
- JWT Authentication
- Pandas
- Scikit-learn
- Prophet
- WebSockets
- ReportLab
- OpenPyXL
- Docker

---

# Frontend

- React.js
- Tailwind CSS
- Axios
- Recharts
- React Router DOM

---

# Project Structure

```bash
AI-DEMAND-FORECASTING/
│
├── backend/
│   ├── app/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── routers/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── utils/
│   │   ├── websocket/
│   │   └── main.py
│   │
│   ├── uploads/
│   ├── reports/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── layouts/
│   │   └── App.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
├── screenshots/
│
└── README.md
```

---

# Backend Setup

# 1. Clone Repository

```bash
git clone <your-github-repository-link>
```

---

# 2. Navigate to Backend

```bash
cd backend
```

---

# 3. Create Virtual Environment

```bash
python -m venv venv
```

---

# 4. Activate Virtual Environment

## Windows

```bash
venv\Scripts\activate
```

## Mac/Linux

```bash
source venv/bin/activate
```

---

# 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 6. Configure Environment Variables

Create a `.env` file inside backend folder.

```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/forecast_db

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

# 7. Run Backend Server

```bash
uvicorn app.main:app --reload
```

Backend runs on:

```bash
http://127.0.0.1:8000
```

Swagger API Docs:

```bash
http://127.0.0.1:8000/docs
```

---

# Frontend Setup

# 1. Navigate to Frontend

```bash
cd frontend
```

---

# 2. Install Dependencies

```bash
npm install
```

---

# 3. Run Frontend

```bash
npm run dev
```

Frontend runs on:

```bash
http://localhost:5173
```

---

# Docker Setup

# Build Docker Image

```bash
docker build -t ai-forecast-api .
```

---

# Run Docker Container

```bash
docker run -p 8000:8000 ai-forecast-api
```

---

# API Modules

# Authentication APIs

- Register User
- Login User
- JWT Authentication
- Role Authorization

---

# Dataset APIs

- Upload Dataset
- Dataset Validation
- Dataset Pagination
- Dataset Search & Filters

---

# Forecast APIs

- Generate Forecast
- Model Comparison
- Forecast History
- Forecast Accuracy Metrics

---

# Dashboard APIs

- Analytics Dashboard
- Sales Trends
- Product Analytics
- Forecast Analytics

---

# Notifications APIs

- Create Notifications
- View Notifications
- Mark Notifications as Read

---

# Admin APIs

- Manage Users
- Monitor Datasets
- Monitor Forecasts
- System Analytics

---

# Reports APIs

- Export Excel Reports
- Export PDF Reports
- Download Analytics Summary

---

# Forecasting Workflow

1. User uploads dataset
2. System validates and cleans dataset
3. Forecast model is trained
4. Future demand predictions are generated
5. Forecast accuracy is calculated
6. Analytics dashboard is updated
7. Reports are generated
8. Notifications are sent to users

---

# Database Features

- Optimized Query Performance
- Indexed Tables
- Forecast History Storage
- Notification Storage
- Role-Based User Tables

---

# Screenshots

## Register Page

![Register](screenshots/register.png)

## Login Page

![Login](screenshots/login.png)

## Dashboard

![Dashboard](screenshots/dashboard.png)

## Dataset Upload

![Upload](screenshots/upload.png)

## Forecast Module

![Forecast](screenshots/forecast.png)

## Reports Module

![Reports](screenshots/reports.png)

## Admin Dashboard

![Admin](screenshots/admin.png)

## Swagger Documentation

![Swagger](screenshots/swagger.png)

---

# Future Improvements

- Cloud Deployment
- Email Notifications
- Dark Mode
- Real-Time Forecast Streaming
- AI Recommendation Engine
- Multi-Tenant Architecture
- Kubernetes Deployment

---

# Author

Manikandan S

