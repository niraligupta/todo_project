# 📝 To-Do List Project (Django + Custom SQLite DB + REST APIs)

A simple To-Do List web application built using **Django**, **custom SQLite CRUD operations (no ORM)**, **HTML templates**, and **RESTful APIs**.  
This project includes:

- CRUD API for tasks  
- Custom database using `sqlite3` (no ORM)  
- HTML templates for adding, editing, and listing tasks  
- Logging + Exception Handling  
- Pytest API tests  
- Clean URL routing  

---

## 🚀 Features

### ✔ API (JSON)
- Create a Task  
- List All Tasks  
- Retrieve Single Task  
- Update a Task  
- Delete a Task  

### ✔ Templates
- `index.html` → Task list  
- `add_task.html` → Add new task  
- `edit_task.html` → Edit only status  

### ✔ Database
- Custom SQLite connection  
- Manual SQL queries (not Django ORM)  
- Auto-create `tasks` table on startup  

### ✔ Testing
- `pytest` tests included  
- Temporary SQLite DB used for tests  
- Covers create, read, update, delete, list operations  

---
# 📂 Project Structure
todo_project/
│── tasks/
│   ├── db.py
│   ├── views.py
│   ├── urls.py
│   ├── templates/
│       ├── index.html
│       ├── add_task.html
│       ├── edit_task.html
│   ├── test_api.py
│
│── todo_project/
│   ├── settings.py
│   ├── urls.py
│
│── manage.py
│── README.md


---

# ⚙️ Installation & Setup

## 1️⃣ Clone Repository

```sh
git clone https://github.com/your-username/todo-list-django.git
cd todo-list-django

python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
## Run the Application
python manage.py runserver

## Database
This project does NOT use Django ORM.

Instead, it uses manual SQLite operations inside:tasks/db.py
The DB is auto-created using:
init_db_if_needed()
📡 API Documentation
📍 Base URL
/api/tasks/
List Tasks

GET /api/tasks/
{
  "tasks": [
    {
      "id": 1,
      "title": "Buy milk",
      "description": "2 liter",
      "due_date": "2025-01-01",
      "status": "pending"
    }
  ]
}
2️⃣ Create Task

POST /api/tasks/

Request Body:
{
  "title": "Buy Groceries",
  "description": "Milk, Eggs",
  "due_date": "2025-12-31",
  "status": "pending"
}
Response:
{
  "task": { ... }
}
3️⃣ Get a Single Task

GET /api/tasks/<id>/

4️⃣ Update a Task

PUT /api/tasks/<id>/

Request body can include any of:
{
  "title": "Updated",
  "description": "Updated desc",
  "status": "done",
  "due_date": "2025-10-10"
}
5️⃣ Delete a Task

DELETE /api/tasks/<id>/

Response:
{ "deleted": true }
Templates (UI Pages)
1️⃣ Home Page → Task List
GET /

2 Edit Task Page
GET /edit/<task_id>/
Running Tests
Tests are located in:
tasks/test_api.py
Run tests:
pytest
Pytest automatically:

Creates temporary DB

Injects into Django settings

Reloads db.py

Tests CRUD

Logging & Exception Handling

Errors inside API are logged using:
logger.exception("Error in tasks_list_create")
This helps with debugging and production logs.




