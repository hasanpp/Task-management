# Task Management Application with Task Completion Report

## Overview
This Task Management Application enables efficient task assignment, management, and reporting. It is role-based with separate privileges for SuperAdmin, Admin, and User. It includes a JWT-based API, admin panel interface for Admins/SuperAdmins, and API endpoints for Users.

## Features

### ✅ JWT Authentication
- Login via `username` and `password` to receive a JWT token.
- Use this token in headers as: 
  ```
  Authorization: Bearer <your_jwt_token>
  ```

### 🔐 Roles & Permissions
- **SuperAdmin**
  - Full control over Admins and Users
  - Assign users to Admins
  - Access all reports and tasks
- **Admin**
  - Can assign tasks to users
  - View/manage only their assigned users and reports
- **User**
  - View their own tasks
  - Update task status
  - Submit task completion report and worked hours

### 📊 Admin Panel (Web Interface)
- SuperAdmins & Admins can log in to access the dashboard.
- SuperAdmin exclusive features:
  - Create/edit/delete users and admins
  - Assign roles and users to admins
- Admin exclusive features:
  - Manage tasks of assigned users
  - View reports of completed tasks

### 📡 User API Endpoints (JWT Secured)

> Base URL: `/tasks/`

| Endpoint | Method | Description |
|---------|--------|-------------|
| `/` | GET | Get all tasks of the logged-in user |
| `/<id>/` | PUT | Update a task status & add report (for users) |
| `/<id>/report/` | GET | Admin/SuperAdmin can fetch task report |

#### 🧪 Example API Usage

**1. Login (JWT Token)**
```
POST /token/
{
    "username": "user1",
    "password": "password123"
}
```
Response:
```
{
    "access": "your_jwt_token",
    "refresh": "your_refresh_token"
}
```

---

**2. Get Assigned Tasks**
```
GET /tasks/
Authorization: Bearer <jwt_token>
```
Response:
```
[
  {
    "id": 1,
    "title": "Fix login bug",
    "description": "Resolve the login issue on production",
    "due_date": "2024-12-01T12:00:00Z",
    "status": "pending"
  }
]
```

---

**3. Update Task Status + Report (Mark as Completed)**
```
PUT /tasks/1/
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
    "status": "completed",
    "completion_report": "Fixed the login issue by updating session logic",
    "worked_hours": 5.5
}
```
Response:
```
{
  "id": 1,
  "status": "completed",
  "completion_report": "Fixed the login issue...",
  "worked_hours": 5.5
}
```

---

**4. View Task Report (Admin/SuperAdmin Only)**
```
GET /tasks/1/report/
Authorization: Bearer <admin_or_superadmin_token>
```
Response:
```
{
  "task_id": 1,
  "completion_report": "Fixed the login issue...",
  "worked_hours": 5.5
}
```

## 🛠️ Technologies Used
- **Backend**: Django, Django REST Framework
- **Authentication**: JWT (via `SimpleJWT`)
- **Database**: SQLite
- **Admin Interface**: Django Admin + Custom Templates

## 🧪 Postman API Documentation
View complete collection:
👉 [Postman Documentation](https://documenter.getpostman.com/view/41192930/2sB2iwGagg)

## 📂 Project Structure
```
TaskManagement/
├── admin_panel/
├── static/
├── TaskManagement/  <-- settings and main urls.py
├── tasks/
├── templates/
├── users/
├── db.sqlite3
├── .env <-- credentials
├── requirements.txt
└── manage.py
```

## ⚙️ Setup Instructions

### 1. Clone the repository
```
git clone "https://github.com/hasanpp/Task-management.git"
cd TaskManagement
```

### 2. Create virtual environment and activate
```
python -m venv env
source env/bin/activate   # On Windows: env\Scripts\activate
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Run the server
```
python manage.py migrate
python manage.py runserver
```

### 5. Superuser (Optional for Admin Panel)
```
python manage.py createsuperuser
```

## 🔐 .env Example
```
SECRET_KEY=<Your Secret Key>
DEBUG=<False/True >
```

## 🧩 Task Model Fields
| Field | Type | Description |
|-------|------|-------------|
| title | CharField | Name of the task |
| description | TextField | Detailed info |
| assigned_to | FK (User) | Assigned user |
| due_date | DateTimeField | Deadline |
| status | Choice | `pending`, `in_progress`, `completed` |
| completion_report | TextField | Submitted by user |
| worked_hours | DecimalField | Tracked work hours |

## 👩‍💼 Roles Summary
| Role | Permissions |
|------|-------------|
| SuperAdmin | All controls |
| Admin | Task management for assigned users |
| User | Manage own tasks, submit reports |

---

## 🧾 Notes
- SQLite is used by default; easy setup.
- Token authentication is required for all `/tasks/` API calls.
- Reports are mandatory when marking a task as completed.

If you face any issues, feel free to reach out!

---

> Developed by: Hasan P P  
> Project Submission for Machine Task  
> © 2025