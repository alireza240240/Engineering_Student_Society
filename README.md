# 📚 Engineering Student Society Management System

🚀 A complete management system for Engineering Student Societies built with **Django + DRF + Celery + Redis**.  
This system helps manage users, articles, news, events, and more — with role-based permissions and an admin dashboard.

---

## ✨ Features

| Feature            | Description |
|--------------------|-------------|
| 👤 **User Management** | Register, login, JWT authentication, roles (Normal / Member / Admin) |
| 📝 **Articles** | Submit, approve/reject by admin, email notifications |
| 📰 **News** | Create/update/delete (Members & Admins only) |
| 🎉 **Events** | Event CRUD, user registration, automatic capacity control |
| 💬 **Comments** | Comment on articles, news, and events |
| 📊 **Admin Dashboard** | Manage users, roles, articles, and events |
| 📑 **API Docs** | Swagger UI & ReDoc via DRF Spectacular |
| ⚡ **Async Tasks** | Celery + Redis for background jobs (e.g., email notifications) |

---

## 🛠️ Technologies Used

- **Backend**: [Django](https://www.djangoproject.com/), [Django REST Framework](https://www.django-rest-framework.org/), [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **Message Broker**: [Celery](https://docs.celeryq.dev/en/stable/) + [Redis](https://redis.io/)
- **API Documentation**: [DRF Spectacular](https://drf-spectacular.readthedocs.io/en/latest/)
- **Email**: SMTP (for system notifications)

---

## 🚀 Quick Start

Get up and running in just a few steps:

```bash
git clone https://github.com/alireza240240/Engineering_Student_Society.git
cd Engineering_Student_Society

# Create environment config
cp .env.example .env   # then fill in your environment variables

# Start DB & Redis with Docker
docker-compose up -d db redis

# Install dependencies
python -m venv venv
source venv/bin/activate   # on Windows use: venv\Scripts\activate
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run the dev server
python manage.py runserver

# For background task processing, run Celery in a separate terminal:
celery -A anjoman_web worker -l info
```

---

## 🌐 API Endpoints
	•	Swagger UI → http://127.0.0.1:8000/api/schema/swagger-ui/
	•	Redoc → http://127.0.0.1:8000/api/schema/redoc/

## Main Endpoints:
	•	/api/acnt/ → User account management (register/login/profile)
	•	/api/news/ → News CRUD
	•	/api/events/ → Event CRUD + registration
	•	/api/articles/ → Article CRUD + approval/rejection
	•	/api/comments/ → Comments on articles, news, and events
	•	/api/dashboard/ → Admin-only dashboard

---

## 🤝 Contributing

Contributions and suggestions are welcome!  

1. Fork this repository  
2. Create a new branch (`git checkout -b feature-name`)  
3. Commit your changes (`git commit -m 'Add new feature'`)  
4. Push to your branch (`git push origin feature-name`)  
5. Open a Pull Request 🎉