# POS Backend (Django)

This is the backend API for a POS system built with Django REST Framework.

---

## 🚀 Features

- User authentication (JWT)
- Billing system
- Customers management
- Payments system
- REST API

---

## 🛠 Tech Stack

- Django 5.x
- Django REST Framework
- SimpleJWT
- SQLite (dev) / PostgreSQL (production)
- Whitenoise

---

## ⚙️ Setup

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver