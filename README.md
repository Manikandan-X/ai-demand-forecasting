# AI Demand Forecasting System

An AI-powered full-stack web application that forecasts future product demand using historical sales datasets and provides business analytics through an interactive dashboard.

---

# Features

## Authentication Module
- User Registration
- User Login
- JWT Authentication
- Protected APIs
- Session Handling

## Dataset Upload Module
- Upload CSV/Excel datasets
- Data validation
- Missing value handling
- Duplicate record removal
- Dataset storage

## AI Forecasting Module
- Dataset preprocessing using Pandas
- Demand forecasting using Machine Learning
- Future sales prediction
- Forecast accuracy calculation

## Dashboard & Analytics
- Total Sales Analytics
- Total Orders Analytics
- Monthly Sales Trends
- Top Products Analysis
- Interactive Charts & Graphs

## Reports Module
- Excel Report Export
- PDF Report Export

## Frontend Features
- Responsive UI
- Protected Routes
- Dynamic Dashboard
- Forecast Visualization
- API Integration

---

# Tech Stack

## Backend
- FastAPI
- MySQL
- SQLAlchemy
- JWT Authentication
- Pandas
- Scikit-learn

## Frontend
- React.js
- Tailwind CSS
- Axios
- Recharts

---

# Project Structure

```bash
AI-Demand-Forecasting/
│
├── backend/
│   ├── app/
│   │   ├── db/
│   │   ├── models/
│   │   ├── routers/
│   │   ├── schemas/
│   │   ├── utils/
│   │   └── main.py
│   │
│   ├── uploads/
│   ├── reports/
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

# Backend Setup

## 1. Clone Repository

```bash
git clone <your-github-repo-link>
```

---

## 2. Navigate to Backend

```bash
cd backend
```

---

## 3. Create Virtual Environment

```bash
python -m venv venv
```

---

## 4. Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

---

## 5. Install Requirements

```bash
pip install -r requirements.txt
```

---

## 6. Configure Environment Variables

Create `.env`

```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/forecast_db

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## 7. Run Backend Server

```bash
uvicorn app.main:app --reload
```

Backend runs on:

```bash
http://127.0.0.1:8000
```

Swagger Docs:

```bash
http://127.0.0.1:8000/docs
```

---

# Frontend Setup

## 1. Navigate to Frontend

```bash
cd frontend
```

---

## 2. Install Dependencies

```bash
npm install
```

---

## 3. Run Frontend

```bash
npm run dev
```

Frontend runs on:

```bash
http://localhost:5173
```

---

# API Modules

## Authentication APIs
- Register User
- Login User
- JWT Token Authentication

## Dataset APIs
- Upload Dataset
- Dataset Validation

## Forecast APIs
- Generate Forecast Predictions

## Dashboard APIs
- Sales Analytics
- Monthly Trends

## Reports APIs
- Export Excel Report
- Export PDF Report

---

# Forecasting Workflow

1. Upload sales dataset
2. Clean and preprocess data
3. Train forecasting model
4. Generate future demand predictions
5. Visualize analytics and forecast charts
6. Export reports

---

# Screenshots

## Register Page
![Register Page](screenshots/register.png)

## Login Page
![Login Page](screenshots/login.png)

## Dashboard
![Dashboard](screenshots/dashboard.png)

## Dataset Upload
![upload](screenshots/upload.png)

## Forecast Visualization
![Forecast](screenshots/forecast.png)

## Reports Module
![reports](screenshots/reports.png)

## Swagger API Documentation
![docs](screenshots/swagger.png)

---

# Future Improvements

- Prophet Forecasting Integration
- Dark Mode
- Advanced Analytics
- Forecast History
- Docker Deployment
- Cloud Deployment
- Email Reports

---

# Author

Manikandan S

---

# License

This project is developed for learning and portfolio purposes.