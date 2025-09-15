# ERISA Claims Management System

A comprehensive Django-based claims management system with modern frontend interface, designed for healthcare claims processing and management.

## 📋 Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Local Development Setup](#local-development-setup)
- [User Management](#user-management)
- [Database Operations](#database-operations)
- [Data Management](#data-management)
- [Deployment](#deployment)
- [API Endpoints](#api-endpoints)
- [Troubleshooting](#troubleshooting)

## ✨ Features

- **Claims Management**: Full CRUD operations for claims with detailed line items
- **User Authentication**: Secure login/logout system with user registration
- **Advanced Search & Filtering**: Search by claim ID, patient name, insurer, status, and policy
- **Financial Summary**: 2x2 grid layout showing total billed, paid, allowed, and claim totals
- **Flagging System**: Flag claims for review with reasons and resolution tracking
- **Notes System**: Add, edit, and delete notes for claims with user attribution
- **CSV Export**: Export claim details with formatted CPT codes and proper filenames
- **Responsive Design**: Mobile-friendly interface with collapsible sidebar
- **Real-time Updates**: HTMX integration for dynamic content without page reloads
- **Analytics Dashboard**: Summary statistics and data visualization
- **Data Monitoring**: Automatic detection of data changes and reload capabilities

## 🛠 Technology Stack

- **Backend**: Django 4.2.7, Python 3.10+
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (development), PostgreSQL (production)
- **Authentication**: Django built-in auth system
- **Styling**: Bootstrap 5 with custom CSS
- **Real-time**: HTMX for dynamic updates
- **Deployment**: Render.com with Gunicorn

## 📁 Project Structure

```
erisa/
├── backend/                     # Django backend application
│   ├── claims/                 # Claims app (models, views, URLs)
│   │   ├── management/         # Custom Django management commands
│   │   │   └── commands/       # Data loading and setup commands
│   │   ├── migrations/         # Database migrations
│   │   ├── models.py           # Database models
│   │   ├── views.py            # View functions
│   │   ├── urls.py             # URL patterns
│   │   └── forms.py            # Form definitions
│   ├── claims_interface/       # Django project settings
│   │   ├── settings.py         # Main settings
│   │   ├── urls.py             # Root URL configuration
│   │   └── wsgi.py             # WSGI configuration
│   ├── manage.py               # Django management script
│   ├── requirements.txt        # Python dependencies
│   └── database.py             # Database utilities
├── frontend/                   # Frontend assets
│   ├── templates/              # Django HTML templates
│   │   ├── base.html           # Base template
│   │   ├── claims/             # Claims-specific templates
│   │   └── registration/       # Authentication templates
│   └── static/                 # CSS, JavaScript, images
│       ├── css/style.css       # Custom styles
│       └── js/data-monitor.js  # Data monitoring script
├── Data/                       # Data files
│   ├── claim_list_data.csv     # Claims list data
│   └── claim_detail_data.csv   # Claims detail data
├── claims.db                   # SQLite database (development)
├── render.yaml                 # Render deployment configuration
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip (Python package installer)
- Git

### 1. Clone the Repository

```bash
git clone <repository-url>
cd erisa
```

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## 🔧 Local Development Setup

### Step 1: Environment Setup

```bash
# Navigate to the project directory
cd erisa

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Navigate to backend directory
cd backend
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser (optional - can be done later)
python manage.py createsuperuser
```

### Step 4: Load Sample Data

```bash
# Load claims data from CSV files
python manage.py load_claims_data

# Or run the complete production setup
python manage.py setup_production
```

### Step 5: Start Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the application.

## 👥 User Management

### Creating Users

#### Method 1: Django Admin Interface
1. Start the development server: `python manage.py runserver`
2. Visit `http://127.0.0.1:8000/admin/`
3. Login with superuser credentials
4. Go to "Users" section
5. Click "Add user" and fill in the details

#### Method 2: Command Line
```bash
# Create superuser
python manage.py createsuperuser

# Create regular user (programmatically)
python manage.py shell
>>> from django.contrib.auth.models import User
>>> user = User.objects.create_user('username', 'email@example.com', 'password')
>>> user.save()
```

#### Method 3: User Registration (Frontend)
1. Visit `http://127.0.0.1:8000/register/`
2. Fill in the registration form
3. Submit to create a new user account

### User Management Commands

```bash
# List all users
python manage.py shell
>>> from django.contrib.auth.models import User
>>> for user in User.objects.all():
...     print(f"Username: {user.username}, Email: {user.email}, Is Staff: {user.is_staff}")

# Change user password
python manage.py changepassword username

# Delete user
python manage.py shell
>>> from django.contrib.auth.models import User
>>> user = User.objects.get(username='username')
>>> user.delete()
```

### User Permissions

- **Superuser**: Full access to admin interface and all features
- **Staff Users**: Can access admin interface but limited permissions
- **Regular Users**: Can access the claims interface, add notes, flag claims

## 🗄️ Database Operations

### Database Models

The system includes four main models:

1. **ClaimList**: Main claims data
2. **ClaimDetail**: Detailed line items for each claim
3. **ClaimFlag**: Flags for claims requiring review
4. **ClaimNote**: Notes added to claims

### Database Migrations

```bash
# Create new migration after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Check migration status
python manage.py showmigrations

# Rollback specific migration
python manage.py migrate claims 0001
```

### Database Management Commands

```bash
# Load claims data from CSV files
python manage.py load_claims_data

# Reload claims data (clear and reload)
python manage.py reload_claims_data

# Auto-reload data when files change
python manage.py auto_reload_data

# Setup production environment
python manage.py setup_production
```

### Database Backup and Restore

```bash
# Backup SQLite database
cp claims.db claims_backup_$(date +%Y%m%d_%H%M%S).db

# Restore from backup
cp claims_backup_20231201_120000.db claims.db

# For PostgreSQL (production)
pg_dump -h hostname -U username -d database_name > backup.sql
psql -h hostname -U username -d database_name < backup.sql
```

## 📊 Data Management

### Loading Data from CSV Files

The system can load data from CSV files in the `Data/` directory:

1. **claim_list_data.csv**: Main claims data
2. **claim_detail_data.csv**: Detailed line items

#### CSV Format Requirements

**claim_list_data.csv** (pipe-delimited):
```
id|patient_name|billed_amount|paid_amount|status|insurer_name|discharge_date
30001|John Doe|1500.00|1200.00|Paid|Blue Cross|2023-01-15
```

**claim_detail_data.csv** (pipe-delimited):
```
id|claim_id|denial_reason|cpt_codes
1|30001|None|99213,99214
2|30001|None|36415
```

### Data Export

#### CSV Export for Individual Claims
- Click "Generate Report" button on claim detail page
- Downloads CSV with filename format: `{claim_id}-{patient_name}.csv`
- Includes all line items with properly formatted CPT codes

#### Bulk Data Export
```bash
# Export all claims to CSV
python manage.py shell
>>> from claims.models import ClaimList
>>> import csv
>>> with open('all_claims.csv', 'w', newline='') as f:
...     writer = csv.writer(f)
...     writer.writerow(['ID', 'Patient Name', 'Status', 'Billed Amount', 'Paid Amount'])
...     for claim in ClaimList.objects.all():
...         writer.writerow([claim.id, claim.patient_name, claim.status, claim.billed_amount, claim.paid_amount])
```

## 🚀 Deployment

### Production Setup

#### Using Render.com (Recommended)

1. **Prepare Repository**:
   - Ensure `render.yaml` is in the root directory
   - Verify `requirements.txt` includes all dependencies

2. **Deploy to Render**:
   - Connect your GitHub repository to Render
   - Render will automatically detect the `render.yaml` configuration
   - Set environment variables in Render dashboard

3. **Environment Variables**:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=.onrender.com
   DATABASE_URL=postgresql://user:password@host:port/database
   ```

#### Manual Production Setup

```bash
# Install production dependencies
pip install gunicorn psycopg2-binary whitenoise

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load initial data
python manage.py load_claims_data

# Start production server
gunicorn claims_interface.wsgi:application
```

### Environment Configuration

#### Development Settings
- `DEBUG=True`
- `SECRET_KEY=development-key`
- Database: SQLite
- Static files: Served by Django

#### Production Settings
- `DEBUG=False`
- `SECRET_KEY=secure-random-key`
- Database: PostgreSQL
- Static files: Served by WhiteNoise or CDN

## 🔌 API Endpoints

### Authentication
- `GET /login/` - Login page
- `POST /login/` - Login form submission
- `GET /logout/` - Logout
- `GET /register/` - Registration page
- `POST /register/` - Registration form submission

### Claims Management
- `GET /` - Dashboard
- `GET /claims/` - Claims list
- `GET /claims/<claim_id>/` - Claim detail
- `GET /claims/<claim_id>/?export=csv` - Export claim as CSV
- `GET /claims/flagged/` - Flagged claims
- `GET /claims/details/` - Claim details list
- `GET /claims/analytics/` - Analytics dashboard

### Notes Management
- `GET /notes/` - Notes list
- `POST /claims/<claim_id>/note/` - Add note
- `GET /notes/<note_id>/edit/` - Edit note
- `POST /notes/<note_id>/delete/` - Delete note

### API Endpoints
- `GET /api/check-changes/` - Check for data changes
- `GET /health/` - Health check
- `GET /debug/` - Debug information

## 🐛 Troubleshooting

### Common Issues

#### 1. Database Connection Issues
```bash
# Check database connection
python manage.py dbshell

# Reset database
rm claims.db
python manage.py migrate
python manage.py load_claims_data
```

#### 2. Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic

# Check static file configuration
python manage.py findstatic css/style.css
```

#### 3. Migration Issues
```bash
# Check migration status
python manage.py showmigrations

# Reset migrations (careful - will lose data)
python manage.py migrate claims zero
python manage.py migrate
```

#### 4. User Authentication Issues
```bash
# Reset user password
python manage.py changepassword username

# Check user permissions
python manage.py shell
>>> from django.contrib.auth.models import User
>>> user = User.objects.get(username='username')
>>> print(user.is_staff, user.is_superuser)
```

### Debug Mode

Enable debug mode for detailed error messages:

```python
# In settings.py
DEBUG = True
```

### Logging

Check Django logs for detailed error information:

```bash
# Run with verbose output
python manage.py runserver --verbosity=2
```

## 📝 Additional Commands

### Development Utilities

```bash
# Check Django setup
python test_basic.py

# Test database connection
python test_django_db.py

# Check database integrity
python manage.py check --database default
```

### Data Management

```bash
# Clear all data
python manage.py shell
>>> from claims.models import *
>>> ClaimList.objects.all().delete()
>>> ClaimDetail.objects.all().delete()
>>> ClaimFlag.objects.all().delete()
>>> ClaimNote.objects.all().delete()

# Count records
python manage.py shell
>>> from claims.models import ClaimList
>>> print(f"Total claims: {ClaimList.objects.count()}")
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
1. Check the troubleshooting section above
2. Review the Django documentation
3. Check the project's issue tracker
4. Contact the development team

---

**Happy Coding! 🚀**