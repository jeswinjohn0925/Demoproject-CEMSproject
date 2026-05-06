# College Event Management System (CEMS)

A comprehensive web application for managing college events with role-based access control.

## Features

### User Roles
- **User**: Regular users who can browse and register for events
- **Staff**: Staff members who can manage event logistics
- **Coordinator**: Event organizers who can create and manage events
- **Admin**: System administrators with full access

### Core Functionality
- User registration and authentication
- Role-based dashboards
- Event creation and management
- Event registration system
- Responsive and attractive UI

## Installation

1. Clone the repository
2. Navigate to the project directory
3. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```
4. Install dependencies:
   ```bash
   pip install django
   ```
5. Run migrations:
   ```bash
   python manage.py migrate
   ```
6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

1. Access the application at `http://127.0.0.1:8000/`
2. Choose your user type from the home page:
   - **Student/User**: Browse and register for events
   - **Staff**: Manage event logistics
   - **Coordinator**: Organize and manage events
   - **Administrator**: Full system access
3. Click Login or Register based on your user type
4. Based on your role, you'll be redirected to the appropriate dashboard
5. Coordinators and admins can create events from their dashboards
6. Users can browse and register for events

## User Registration

- **Students/Users**: Register through the website
- **Staff**: Register through the website
- **Coordinators**: Register through the website
- **Administrators**: Must be created via terminal by system administrators

## Default Admin Credentials

- Username: `admin`
- Password: `admin123`
- Email: `admin@example.com`

## Technologies Used

- Django 5.1
- Bootstrap 5
- Font Awesome
- SQLite (default database)

## Project Structure

```
CEMSproject/
├── CEMSproject/          # Main Django project
├── accounts/             # User management app
├── events/               # Event management app
├── templates/            # HTML templates
├── static/               # Static files (CSS, JS, images)
└── db.sqlite3           # Database file
```