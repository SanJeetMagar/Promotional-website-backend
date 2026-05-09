# Promotional Website Backend

A Django REST backend for a promotional website. The project exposes APIs for the homepage, company information, products, gallery, FAQ, contact form, and collaboration content, with Swagger and ReDoc documentation built in.

## Features

- Django REST Framework API with JSON responses
- Swagger UI and ReDoc API documentation
- Modular apps for homepage, company info, products, gallery, FAQ, contact, and collab content
- Media file support for uploaded images and documents
- CORS enabled for frontend integration
- Email configuration for contact workflows
- Celery support for background tasks

## Tech Stack

- Python 3
- Django
- Django REST Framework
- drf-spectacular
- Celery and Redis
- SQLite for local development

## Project Structure

- `config/` - Django project settings, URLs, ASGI, WSGI, and Celery configuration
- `src/app/` - Feature apps and shared utilities
- `static/` - Static assets
- `media/` - User-uploaded files

## Getting Started

### 1. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root and add the required values:

```env
SECRET_KEY=your-secret-key
DEBUG=True
SITE_NAME=YourSiteName

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-app-password
CONTACT_ADMIN_EMAIL=admin@example.com
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Create a superuser

```bash
python manage.py createsuperuser
```

### 6. Start the development server

```bash
python manage.py runserver
```

## API Documentation

After starting the server, open:

- Swagger UI: `/`
- Swagger JSON schema: `/api/schema/`
- Swagger UI alternative: `/api/docs/`
- ReDoc: `/api/redoc/`

## Core API Areas

- `/api/v1/` - Homepage, company info, products, gallery, and contact endpoints
- `/api/v1/faq/` - FAQ endpoints
- `/api/v1/collab/` - Collaboration endpoints

## Notes

- SQLite is used by default, so no database service is required for local development.
- Media uploads are stored in the `media/` directory.
- If you use Celery, make sure Redis is available and configured in your environment.


