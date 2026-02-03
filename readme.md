# 🧪 Chemical Equipment Analytics Dashboard  
### **Web + Desktop Dataset Visualization System**

A full-stack analytics dashboard that allows users to upload chemical equipment datasets (CSV), view summary statistics, visualize equipment distributions using charts, download professional PDF reports, and maintain upload history separately for each authenticated user.

This project was developed as part of a **Screening Task Submission** requiring:

✅ React Web Frontend  
✅ Desktop Application (PyQt5)  
✅ Django REST Backend  
✅ SQLite Database Storage  
✅ User Authentication + Per-User Upload History  
✅ Professional Report Generation (PDF + Charts + Data Tables)

---

---

## 📌 Project Overview

This system provides a complete workflow:

1. **User Signup/Login**
2. Upload a CSV dataset containing chemical equipment parameters
3. Auto-generate analytics such as:

   - Total Equipment Count  
   - Average Flowrate  
   - Average Pressure  
   - Average Temperature  
   - Equipment Type Distribution  

4. Display results inside both interfaces:

   ✅ Summary Cards  
   ✅ Charts (Bar + Pie)  
   ✅ Dataset Preview Table  
   ✅ Upload History (Last 5 uploads per user)

5. Download a **multi-page professional PDF report** containing:

   - Title & Metadata  
   - Summary Tables  
   - Dataset Preview  
   - Professional Charts  

---

---

## ⚙️ Tech Stack Used

| Layer        | Technology |
|-------------|------------|
| Backend API  | Django + Django REST Framework |
| Database     | SQLite3 |
| Auth System  | Token Authentication |
| Web Frontend | React + Chart.js |
| Desktop App  | PyQt5 + Matplotlib |
| Analytics and data handling    | Pandas |
| Charts       | Matplotlib & Chart.js|
| PDF Reports  | ReportLab |

---

---

## 📂 Project Structure

```bash
Equipment_Analytics_Dashboard/
│
├── backend/                # Django Backend
│   ├── equipment/          # Core API app
│   │   ├── models.py       # DatasetUpload model (linked to users)
│   │   ├── views.py        # Upload + History + Report + Signup APIs
│   │   ├── analytics.py    # CSV analytics logic
│   │   ├── report.py       # Professional PDF report generator
│   │   └── serializers.py
│   │
│   ├── backend/            # Django settings + URLs
│   └── db.sqlite3          # SQLite Database
│
├── web-frontend/           # React Web Frontend
│   ├── src/
│   │   ├── components/     # Login, Signup, Upload, Charts, History
│   │   ├── api.js          # Axios Token API setup
│   │   └── App.jsx
│   └── package.json
│
├── desktop-app/            # PyQt5 Desktop Dashboard
│   ├── ui.py               # Full UI (Login + Dashboard)
│   ├── api.py              # Backend API connection
│   ├── charts.py           # Modern chart rendering
│   └── main.py             # Entry point
│
└── sample_equipment_data.csv
```
# 🏗️ Multi-Platform Analytics & Reporting System

![Status](https://img.shields.io/badge/status-completed-success)
![Platform](https://img.shields.io/badge/platform-Web%20%7C%20Desktop-blue)
![Backend](https://img.shields.io/badge/backend-Django%20REST-green)

A robust full-stack solution featuring a unified backend for both Web and Desktop applications, providing secure authentication, dataset analytics, and automated PDF report generation.

---

## ✅ Features Implemented

### 🔐 Authentication System
Signup and Login are fully supported across both platforms:
* ✅ **Web Frontend** (React)
* ✅ **Desktop App** (PyQt5)
* **Secure Storage:** Passwords hashed using Django’s internal hashing algorithms.
* **Security:** Token-based authentication ensures all data access is protected.

### 📤 Dataset Upload System
Users can upload CSV files containing technical parameters:
* **Fields:** `Type`, `Flowrate`, `Pressure`, `Temperature`
* **Validation:** Backend automatically validates required columns.
* **Storage:** Saves dataset files and metadata summaries in **SQLite**.

### 📊 Analytics Dashboard
Real-time visualization after every successful upload:
* ✅ **Summary Statistics Cards**
* ✅ **Equipment Distribution Charts** (Bar/Pie)
* ✅ **Dataset Preview Table** (Displaying first 10 rows)
* ✅ **Upload History:** Tracks the last 5 uploads per user.

### 🧾 Professional PDF Reports
Downloadable reports featuring:
* **Metadata:** Title page and dataset context.
* **Analysis:** Summary tables and distribution charts.
* **Formatting:** Clean tabular previews of data.
* *Accessible from both Web and Desktop dashboards.*

---

## 🚀 Setup & Installation Guide

### ✅ Backend Setup (Django REST API)
1.  **Navigate to backend folder:**
    ```bash
    cd backend
    ```
2.  **Create virtual environment:**
    ```bash
    python -m venv venv
    # Activate (Mac/Linux):
    source venv/bin/activate
    # Activate (Windows):
    venv\Scripts\activate
    ```
3.  **Install requirements:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Apply migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
5.  **Run backend server:**
    ```bash
    python manage.py runserver
    ```
    *Backend starts at:* `http://127.0.0.1:8000/`

### ✅ Web Frontend Setup (React)
1.  **Navigate to frontend folder:**
    ```bash
    cd web-frontend
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```
3.  **Run development server:**
    ```bash
    npm run dev
    ```
    *Frontend runs at:* `http://localhost:5173/`

### ✅ Desktop Application Setup (PyQt5)
1.  **Navigate to desktop app folder:**
    ```bash
    cd desktop-app
    ```
2.  **Install required packages:**
    ```bash
    pip install pyqt5 requests matplotlib pandas
    ```
3.  **Run desktop dashboard:**
    ```bash
    python main.py
    ```

---

## ✅ Usage Instructions

1.  **Signup:** Create an account via either the Web or Desktop interface.
2.  **Login:** Securely sign in to access your personal dashboard.
3.  **Upload Dataset:** Use a CSV with the following structure:
    ```csv
    Type,Flowrate,Pressure,Temperature
    Pump,20,15,50
    Valve,12,10,40
    Heater,18,12,55
    ```
4.  **View Analytics:** View summary stats, preview tables, and distribution charts instantly.
5.  **History:** View your last 5 uploads (older uploads are automatically cleared per user).
6.  **Download PDF:** Click the "Download Report" button on either platform.

---

## ✅ Screening Task Compliance Checklist

| Task Requirement | Status |
| :--- | :--- |
| React Web Dashboard | ✅ Completed |
| PyQt5 Desktop Dashboard | ✅ Completed |
| Authentication + Signup/Login | ✅ Completed |
| SQLite Integration | ✅ Completed |
| Dataset Upload + Preview Table | ✅ Completed |
| Charts Visualization | ✅ Completed |
| PDF Report Generation | ✅ Completed |
| Last 5 Upload History per User | ✅ Completed |
| Token Protected Reports | ✅ Completed |

---

## 📌 Future Improvements
* **Enhanced Navigation:** Further modularize React Router for `/login`, `/signup`, and `/dashboard`.
* **Report Layouts:** Implement Platypus layouts for more complex PDF designs.
* **Data Browsing:** Add pagination to browse full datasets beyond the preview.
* **Deployment:** Host backend and frontend on cloud platforms.

---

## 👩‍💻 Author
**Jahnvi Verma**
*Computer Science Student | Full Stack Developer*
*Built for Screening Task Submission* ✅
