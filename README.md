# TCE Placement Portal

A role-based Placement Management System built using Flask, SQLAlchemy, and Bootstrap.

The platform simplifies campus recruitment by providing a centralized portal where students can discover opportunities, companies can manage hiring processes, and administrators can oversee placement activities through a single application.

---

## Overview

Managing placement activities manually can be time-consuming and difficult to scale. This project aims to streamline the recruitment workflow by connecting students, recruiters, and administrators through an integrated web application.

The system follows a role-based architecture with dedicated dashboards and functionalities for each user type.

---

## Key Features

### Student Portal

* Manage academic profile and resume
* Browse available placement drives
* Apply for eligible opportunities
* Track application progress

### Company Portal

* Register and maintain company profile
* Create and manage placement drives
* Review applicants
* Shortlist, select, or reject candidates

### Admin Portal

* Manage students and companies
* Approve or reject company registrations
* Approve or reject placement drives
* Monitor placement activities across the platform

---

## Tech Stack

### Backend

* Python
* Flask
* Flask-Login
* SQLAlchemy

### Frontend

* HTML
* CSS
* Bootstrap 5
* Jinja2

### Database

* SQLite

---

## System Workflow

```text
Student
   │
   ▼
Complete Profile
   │
   ▼
Browse Drives
   │
   ▼
Apply for Drive
   │
   ▼
Company Reviews Application
   │
   ├── Shortlisted
   ├── Selected
   └── Rejected
   │
   ▼
Student Tracks Status
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/tce-placement-portal.git
cd tce-placement-portal
```

### Create a Virtual Environment

```bash
python -m venv venv
```

### Activate the Environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## Project Structure

```text
tce-placement-portal/
│
├── app.py
├── extensions.py
├── requirements.txt
│
├── models/
├── routes/
├── templates/
├── static/
│
└── README.md
```

---

## Screenshots

Add screenshots of:

* Login Page
* Student Dashboard
* Company Dashboard
* Admin Dashboard
* Placement Drive Management

---

## Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature-name
```

3. Commit your changes

```bash
git commit -m "Add feature"
```

4. Push to GitHub

```bash
git push origin feature-name
```

5. Open a Pull Request

Please ensure that your changes are properly tested and follow the existing project structure.

---

## Future Enhancements

* Email notifications
* Placement analytics dashboard
* Interview scheduling
* Advanced search and filtering
* Cloud database integration
* Containerized deployment using Docker

