# HRMS Backend

A Django REST Framework based Human Resource Management System (HRMS) that provides a complete recruitment platform for candidates, employers, and administrators. The system includes AI-powered interview screening, ATS resume matching, subscription management, payment integration, analytics, and automated recruitment workflows.

---

## Features

### Authentication

* JWT Authentication
* User Registration & Login
* Token Refresh & Logout
* Role-based Access Control (Admin, Employer, Candidate)

### Candidate Module

* Candidate Profile Management
* Resume Upload
* Job Search & Recommendations
* Save Jobs
* Apply for Jobs
* Application Tracking
* Candidate Dashboard

### Employer Module

* Employer Profile Management
* Job Posting & Management
* Applicant Management
* Job Analytics
* Recent Applications
* Job Status Control

### ATS (Applicant Tracking System)

* Resume Parsing
* ATS Score Calculation
* Candidate Ranking
* Automatic Shortlisting
* Automatic Rejection

### AI Interview Module

* AI Interview Question Generation
* Answer Evaluation
* AI Interview Reports
* Recruiter Analytics
* Interview Scheduling
* Interview Reminders

### Payment & Subscription

* Razorpay Payment Gateway
* Subscription Management
* Premium Analytics
* Transaction Management
* Revenue Reports

### Admin Module

* Employer Approval
* User Management
* User Flagging
* Job Moderation
* Spam Job Removal
* System Logs
* Platform Analytics

---

## Technology Stack

* Python
* Django
* Django REST Framework
* PostgreSQL
* JWT Authentication
* Google Gemini API
* Razorpay
* Render
* Gunicorn
* Swagger (drf-spectacular)

---

## Project Structure

```
apps/
    ai/
    applications/
    ats/
    jobs/
    notifications/
    payments/
    users/

services/

zecser_project/

manage.py
requirements.txt
```

---

## Installation

Clone the repository

```bash
git clone <repository_url>
cd hrms-backend
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Configure environment variables

Create a `.env` file and add the required environment variables.

Run migrations

```bash
python manage.py migrate
```

Start the development server

```bash
python manage.py runserver
```

---

## Deployment

* Platform: Render
* Database: PostgreSQL
* Application Server: Gunicorn
* Environment Variables managed securely through Render

---

## Security

* JWT Authentication
* Role-based Authorization
* Environment Variable Configuration
* PostgreSQL Database
* Production Deployment
* API Rate Limiting Support

---


## Author

**Muhammad Midlaj**
