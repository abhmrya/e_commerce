# 🛒 Django E-Commerce Website (DRF + JWT + Google OAuth + Celery)

A full-featured **E-Commerce platform** built with Django & Django REST Framework, packed with modern authentication, role-based access, async task handling, and a clean Tailwind CSS UI.

---

## ✨ Features

### 🔑 Authentication & Security
- JWT authentication with auto token expiry & logout
- Session-based login support
- Google Social Login (OAuth2)
- Email notifications for registration & login

### 👥 User Roles & Permissions
- **Admin**:
  - Full control (add, edit, delete, view all products)
  - Manage users
- **Customer**:
  - Edit profile & delete account
  - Add products to cart & purchase
  - Download receipts instantly
- Only logged-in users can shop and use cart

### 🛍️ E-Commerce
- Product listing & cart management
- Instant PDF receipt generation for orders

### 📊 Request Tracking
Logs important request details for monitoring & debugging:
- IP address of the user
- Request time
- HTTP method (GET/POST)
- Request path (API endpoint accessed)
- User-Agent (browser/device info)

### ⚡ Async & Efficient
- Celery + Redis for background email sending & task processing

---

## 🛠 Tech Stack
- **Backend:** Django, Django REST Framework
- **Auth:** JWT, Google OAuth2
- **Async Tasks:** Celery + Redis
- **Frontend:** Tailwind CSS
- **Database:** (PostgreSQL/MySQL/SQLite – specify which one you used)

---

## 🚀 Installation
### 1️⃣ Clone the Repository
```bash
``` git clone https://github.com/abhaymaurya57/e_commerce.git```
cd e_commerce
2️⃣ Create Virtual Environment & Install Dependencies

```python -m venv venv```
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt```
3️⃣ Run Migrations

```python manage.py migrate```
4️⃣ Start Redis Server (for Celery tasks)

```redis-server```
5️⃣ Start Celery Worker

```celery -A project_name worker -l info```
Replace project_name with your Django project’s name.

6️⃣ Run the Development Server

```python manage.py runserver```
7️⃣ Access in Browser
👉``` http://127.0.0.1:8000/```

