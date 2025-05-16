# 🎓 IUM Analyst Programmer Challenge – Backend

Welcome to the **Backend Repository** for the Analyst Programmer Technical Challenge. This repository will host your backend solution for the **Student Registration Dashboard**.

## 👤 Candidate Details

Please fill in your details **accurately** as they appear on your CV:

- **Full Name**: Collin Nehemia
- **Email Address**: collinnadilu@gmail.com 
- **Phone Number**: +264 81 5713080 
- **Other Information (Optional)**: https://www.linkedin.com/in/collin-nehemia-05643520a/

⚠️ **Failure to include accurate personal information will result in disqualification.**

---

## 🔀 Branching Instructions

Before you begin, **create a new branch** from `main` using the following format: challenge-CANDIDATE-FULL-NAME
> Example:  
> `challenge-John-Doe`

Push all your work and open a **pull request (PR)** from your branch to `main` before the deadline.

---

## 📜 Task Overview

You are required to:
- Load the provided dataset into **PostgreSQL**.
- Create a RESTful API using **Python (FastAPI or Flask)**.
- Implement endpoints such as:
  - `/api/total-registrations`
  - `/api/registrations-by-programme`
  - `/api/registrations-by-school`
  - `/api/registrations-by-year`
  - `/api/top-schools`

Refer to the printed challenge brief for full requirements.

---

## 📄 Submission Checklist

- [ ] All endpoints implemented and tested
- [ ] `README.md` completed with full contact information
- [ ] PR opened from your named branch
- [ ] Code is clean, organized, and committed meaningfully
- [ ] Optional: Demo available for invigilators

---

## 🔒 Rules Reminder

- No external help or collaboration allowed
- You must use your own device and internet connection
- All code must be written and submitted during the challenge session
- You may use AI Assistants such as ChatGPT

---

**Good luck!**  
*Centre for Digital Initiatives – IUM*


## 🚀 How to Run the Backend

### Prerequisites
- Python 3.8+ installed
- PostgreSQL database server installed and running

### Setup and Installation

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     cd challenge-ap-backend 
     source venv/bin/activate && python3 main.py
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database connection**:
   - The application will use PostgreSQL by default
   - Database connection settings can be modified in the `database.py` file

5. **Run the application**:
   ```bash
   python main.py
   ```

The backend API will be available at `http://localhost:8000`.

### Available API Endpoints

- `GET /api/total-registrations` - Get total number of registrations
- `GET /api/registrations-by-programme` - Get registrations grouped by programme
- `GET /api/registrations-by-year` - Get registrations grouped by academic year
- `GET /api/top-schools` - Get top secondary schools by student count
- `GET /api/registrations-by-gender` - Get registrations grouped by gender
- `GET /api/registrations` - Get detailed registration records
- `GET /api/students` - Get formatted student records

Each endpoint supports filtering by academic year (including `null` for unspecified) and programme.

---

