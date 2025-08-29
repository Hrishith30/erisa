# ERISA Claims Management System

A comprehensive Django-based claims management system with modern frontend interface.

## Project Structure

```
erisa/
├── backend/                 # Django backend application
│   ├── claims/             # Claims app (models, views, URLs)
│   ├── claims_interface/   # Django project settings
│   ├── manage.py           # Django management script
│   ├── requirements.txt    # Python dependencies
│   └── database.py         # Database utilities
├── frontend/               # Frontend assets
│   ├── templates/          # Django HTML templates
│   └── static/             # CSS, JavaScript, images
├── Data/                   # Data files
├── claims.db               # SQLite database
└── README.md               # This file
```

## Quick Start

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend Development
The frontend templates and static files are located in the `frontend/` directory and are automatically served by Django.

## Features

- **Claims Management**: Full CRUD operations for claims
- **User Authentication**: Secure login/logout system
- **Search & Filtering**: Advanced search capabilities
- **Pagination**: Efficient data browsing
- **Responsive Design**: Mobile-friendly interface
- **Real-time Updates**: HTMX integration for dynamic content

## Technology Stack

- **Backend**: Django 4.2.7, Python 3.10+
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (development), PostgreSQL (production)
- **Authentication**: Django built-in auth system
- **Styling**: Bootstrap 5 with custom CSS

## Development

### Backend Development
- All Django code is in the `backend/` directory
- Use `python manage.py` commands from the backend directory
- Database migrations and models are in `backend/claims/`

### Frontend Development
- Templates are in `frontend/templates/`
- Static files (CSS, JS) are in `frontend/static/`
- Changes to templates/static files are automatically detected

## Deployment

The system is configured for deployment on Render with:
- Automatic static file collection
- WhiteNoise for static file serving
- Environment variable configuration
- Production security settings

## Contributing

1. Make changes in the appropriate directory (backend/ or frontend/)
2. Test your changes locally
3. Update documentation as needed
4. Submit pull requests

## License

This project is proprietary software.
