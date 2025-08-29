# Project Structure Documentation

## Overview
The ERISA Claims Management System has been reorganized into a clear separation of frontend and backend components for better maintainability and development workflow.

## Directory Structure

```
erisa/
├── backend/                 # Django backend application
│   ├── claims/             # Claims app (models, views, URLs)
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── management/
│   │       └── commands/
│   ├── claims_interface/   # Django project settings
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── middleware.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── manage.py           # Django management script
│   ├── requirements.txt    # Python dependencies
│   ├── database.py         # Database utilities
│   ├── debug_db.py         # Debug utilities
│   └── check_db.py         # Database checking utilities
├── frontend/               # Frontend assets
│   ├── templates/          # Django HTML templates
│   │   ├── base.html
│   │   ├── 400.html
│   │   ├── 403.html
│   │   ├── 404.html
│   │   ├── 500.html
│   │   └── claims/
│   │       ├── analytics.html
│   │       ├── claim_detail.html
│   │       ├── claim_detail_partial.html
│   │       ├── claim_details_list.html
│   │       ├── claim_details_list_partial.html
│   │       ├── claim_list.html
│   │       ├── claim_list_partial.html
│   │       └── edit_note.html
│   └── static/             # CSS, JavaScript, images
│       └── css/
│           └── style.css
├── Data/                   # Data files
├── claims.db               # SQLite database
├── build.sh                # Unix/Linux build script
├── build.bat               # Windows build script
├── dev.sh                  # Unix/Linux development script
├── dev.bat                 # Windows development script
├── README.md               # Main project documentation
├── STRUCTURE.md            # This file
└── .gitignore              # Git ignore rules
```

## Key Changes Made

### 1. Backend Organization (`backend/`)
- **Django Project**: All Django code is now in the `backend/` directory
- **Settings Updated**: Template and static file paths updated to point to frontend
- **Database Path**: Updated to reference database from parent directory
- **Virtual Environment**: Will be created in `backend/` directory

### 2. Frontend Organization (`frontend/`)
- **Templates**: All Django HTML templates moved to `frontend/templates/`
- **Static Files**: CSS, JavaScript, and images moved to `frontend/static/`
- **Automatic Serving**: Django automatically serves these files

### 3. Build Scripts
- **`build.sh`**: Unix/Linux build script
- **`build.bat`**: Windows build script
- **`dev.sh`**: Unix/Linux development startup script
- **`dev.bat`**: Windows development startup script

## Development Workflow

### Initial Setup
1. **Run Build Script**: Execute `build.bat` (Windows) or `build.sh` (Unix/Linux)
2. **Virtual Environment**: Script creates and activates virtual environment
3. **Dependencies**: Installs all Python requirements
4. **Database**: Runs migrations and sets up database
5. **Static Files**: Collects and organizes static files

### Daily Development
1. **Start Development**: Run `dev.bat` (Windows) or `dev.sh` (Unix/Linux)
2. **Backend Changes**: Edit files in `backend/` directory
3. **Frontend Changes**: Edit files in `frontend/` directory
4. **Automatic Reload**: Django automatically detects changes

### File Locations

#### Backend Development
- **Models**: `backend/claims/models.py`
- **Views**: `backend/claims/views.py`
- **URLs**: `backend/claims/urls.py`
- **Settings**: `backend/claims_interface/settings.py`
- **Database**: `backend/claims/management/commands/`

#### Frontend Development
- **Templates**: `frontend/templates/`
- **CSS**: `frontend/static/css/style.css`
- **JavaScript**: Inline in templates or separate files in `frontend/static/js/`
- **Images**: `frontend/static/images/`

## Benefits of New Structure

### 1. Clear Separation
- **Backend**: All Django/Python code in one place
- **Frontend**: All templates and static files in one place
- **Easy Navigation**: Developers know exactly where to find files

### 2. Better Collaboration
- **Frontend Developers**: Work exclusively in `frontend/` directory
- **Backend Developers**: Work exclusively in `backend/` directory
- **Reduced Conflicts**: Less chance of accidentally editing wrong files

### 3. Easier Deployment
- **Backend**: Can be deployed separately (Docker, virtual environment)
- **Frontend**: Can be served by CDN or separate web server
- **Scalability**: Backend and frontend can scale independently

### 4. Development Workflow
- **Hot Reload**: Django automatically detects template changes
- **Static Files**: Changes to CSS/JS are immediately visible
- **Clear Commands**: Simple scripts for common tasks

## Migration Notes

### What Changed
1. **File Locations**: All Django files moved to `backend/`
2. **Template Paths**: Updated in Django settings
3. **Static File Paths**: Updated in Django settings
4. **Database Path**: Updated to work from new structure

### What Stayed the Same
1. **Functionality**: All features work exactly the same
2. **URLs**: All URLs and routing remain unchanged
3. **Database**: Same database structure and data
4. **User Experience**: No changes to the user interface

## Troubleshooting

### Common Issues

#### 1. "Module not found" errors
- **Solution**: Make sure you're running commands from `backend/` directory
- **Check**: Verify `manage.py` exists in `backend/`

#### 2. Template not found errors
- **Solution**: Check that templates are in `frontend/templates/`
- **Check**: Verify Django settings point to correct template directory

#### 3. Static files not loading
- **Solution**: Run `python manage.py collectstatic` from `backend/` directory
- **Check**: Verify static files are in `frontend/static/`

#### 4. Database connection errors
- **Solution**: Ensure `claims.db` is in the project root directory
- **Check**: Verify database path in `backend/claims_interface/settings.py`

### Getting Help
1. **Check Structure**: Verify files are in correct directories
2. **Run Build Script**: Use `build.bat` or `build.sh` to reset environment
3. **Check Settings**: Verify Django settings point to correct paths
4. **Read Logs**: Check Django error logs for specific error messages

## Future Enhancements

### Potential Improvements
1. **API Separation**: Move to REST API with separate frontend framework
2. **Microservices**: Split backend into multiple services
3. **Frontend Framework**: Integrate React, Vue, or Angular
4. **Containerization**: Docker support for easier deployment

### Current Benefits
1. **Maintainability**: Clear separation of concerns
2. **Scalability**: Easy to scale components independently
3. **Development Speed**: Faster development with clear file organization
4. **Team Collaboration**: Better workflow for multiple developers

## Conclusion

The new structure provides a solid foundation for future development while maintaining all existing functionality. The separation of frontend and backend makes the codebase more maintainable and easier to work with for development teams.
