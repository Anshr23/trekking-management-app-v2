# Trekking Management Application V2

Trekking Management Application V2 (TMA-V2) is a full-stack web application developed as part of the Modern Application Development II course.

The application provides a centralized platform for managing trekking activities involving three different types of users:

- Admin
- Trek Staff
- Trekker

The system allows administrators to manage treks, staff members, users, bookings, and analytics. Trek Staff can manage their assigned treks and participants, while Trekkers can explore available treks, make bookings, track booking status, and view their complete trekking history.

---

## Features

### Admin

- Pre-created Admin account with no public registration.
- Dashboard showing total treks, trekkers, staff members, bookings, active treks, and completed treks.
- Create, update, delete, search, and filter treks.
- Create and manage Trek Staff accounts.
- Assign Trek Staff members to specific treks.
- View and manage all registered users.
- Deactivate or blacklist users and staff members.
- View all booking records.
- View analytics and trekking statistics using interactive charts.

### Trek Staff

- Login using an account created by the Admin.
- View only the treks assigned by the Admin.
- View the number of registered participants for assigned treks.
- View and manage participant lists.
- Update available trek slots.
- Update trek status.
- Mark treks as started or completed.
- Access restrictions ensure that staff members can manage only their assigned treks.

### Trekker

- Self-registration and login.
- View available and open treks.
- Search and filter treks by difficulty, location, and duration.
- Book available treks.
- View current bookings and booking status.
- Cancel bookings where applicable.
- View complete trekking history.
- Update profile information.
- Export trekking history as a CSV file.

---

## Core Functionalities

- JWT-based authentication and authorization.
- Role-based access control for Admin, Trek Staff, and Trekkers.
- Unified User model for all three roles.
- Prevention of duplicate trek bookings.
- Prevention of overbooking beyond available slots.
- Booking allowed only when a trek is Open.
- Complete booking and trekking history management.
- Staff-level access restrictions for assigned treks.
- Search and filtering functionality.
- Backend and frontend validation.
- Responsive user interface.

---

## Background Jobs

The application uses Celery with Redis to implement asynchronous and scheduled background jobs.

### Daily Trek Reminders

A scheduled Celery task checks for upcoming treks and sends email reminders to registered participants with trek information and the scheduled start date.

### Monthly Admin Activity Report

A scheduled task generates a monthly HTML activity report containing:

- Number of treks conducted.
- Total number of participants.
- Most popular trek.

The generated report is automatically sent to the Admin through email.

### Asynchronous CSV Export

Trekkers can trigger an asynchronous job to export their complete trekking history as a CSV file.

The export contains:

- User ID
- Trek name
- Location
- Booking status
- Booking date
- Trek start date
- Trek end date

The Celery worker processes the export asynchronously and the user is notified when the file is ready.

---

## Redis Caching

Redis caching is used to improve API performance for frequently accessed trek data.

The implementation includes:

- Caching of frequently accessed trek listings.
- Cache expiration.
- Cache invalidation when trek information is modified.
- Redis as the Celery message broker and result backend.

---

## Analytics

The Admin dashboard includes analytics and visualizations implemented using Chart.js.

Available analytics include:

- Trek popularity.
- Booking status distribution.
- Monthly booking trends.
- Trek status distribution.

---

## Technology Stack

| Technology / Library | Purpose |
|---|---|
| Flask | REST API backend framework |
| Vue.js | Frontend user interface |
| SQLAlchemy | Object Relational Mapper for database operations |
| SQLite | Relational database |
| Bootstrap 5 | Responsive frontend styling |
| JWT / Flask-JWT-Extended | Authentication and role-based authorization |
| Axios | Communication between Vue.js frontend and Flask APIs |
| Redis | API caching and Celery message broker |
| Celery | Asynchronous background jobs |
| Celery Beat | Scheduled background tasks |
| Flask-Mail | Email reminders and monthly Admin reports |
| Flask-Caching | Redis-based API caching |
| Chart.js | Admin analytics and data visualization |
| Flask-CORS | Cross-origin communication between frontend and backend |

---

## Database Models

The application uses four main database tables:

### User

Stores account and authentication information for Admin, Trek Staff, and Trekkers.

### Staff Profile

Stores additional information about Trek Staff members, including experience, specialization, emergency contact, biography, and status.

### Trek

Stores trekking event information such as trek name, location, difficulty, duration, altitude, slots, price, assigned staff, status, and dates.

### Booking

Stores booking records connecting Trekkers with treks and maintains booking status and trekking history.

---

## Authentication and Roles

The application uses JWT-based authentication.

After successful login, a JWT access token is generated and sent with protected API requests.

The three supported roles are:

1. Admin
2. Trek Staff
3. Trekker

Each role has access only to authorized resources and operations.

---

## Running the Application

### 1. Start Redis

```bash
redis-server
Verify Redis:

redis-cli ping

Expected output:

PONG
2. Start the Flask Backend

Navigate to the backend directory:

cd backend

Activate the virtual environment:

source env/bin/activate

Run the Flask application:

python app.py

The backend runs at:

http://127.0.0.1:5001
3. Start the Vue.js Frontend

Navigate to the frontend directory:

cd frontend

Install dependencies if required:

npm install

Start the development server:

npm run dev

The frontend normally runs at:

http://localhost:5173
4. Start the Celery Worker

From the backend directory with the virtual environment activated:

celery -A celery_worker.celery worker --loglevel=info
5. Start Celery Beat

In another terminal:

celery -A celery_worker.celery beat --loglevel=info
Environment Variables

Create a .env file inside the backend directory with the required email configuration:

MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-google-app-password
ADMIN_REPORT_EMAIL=admin-email@example.com

Do not commit real email credentials or application passwords to a public repository.

API Architecture

The Vue.js frontend communicates with the Flask backend using REST APIs through Axios.

Major API groups include:

/api/auth - Authentication and registration.
/api/admin - Admin dashboard, analytics, treks, users, staff, and bookings.
/api/staff - Staff dashboard and assigned trek management.
/api/trekker - Trek discovery, booking, history, profile, and CSV export.
Project Highlights
Three-role authentication and authorization system.
Complete trek and booking management.
Staff assignment and participant management.
Redis API caching.
Celery asynchronous tasks.
Celery Beat scheduled tasks.
Automated email reminders.
Monthly Admin reports through email.
Asynchronous CSV export.
Interactive Chart.js analytics dashboard.
Responsive Vue.js and Bootstrap user interface.
Author

Ansh Rai