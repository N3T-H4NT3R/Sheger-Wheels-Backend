# Sheger Wheels — Backend API

Sheger Wheels is a car rental platform backend built with **Django** and **Django REST Framework (DRF)**. It provides APIs for user authentication, car listings, bookings, balance recharge, refunds, and rental dashboards.

## Features

- User registration and JWT authentication
- User profile management
- Public car listings and individual car details
- Owner-specific car listings
- Car rental booking management
- Booking status updates by car owners
- Balance recharge and refund records
- Owner rental dashboard with booking and income summaries
- Permission-protected endpoints

## Technology Stack

- Python
- Django
- Django REST Framework
- Simple JWT
- Database: Configure the database specified in your Django settings

## Project Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd <your-project-directory>
```

### 2. Create and activate a virtual environment

On Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

If the project contains a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file if your project uses environment variables. Configure the required database credentials, Django secret key, debug mode, and other project settings.

**Security:** Do not commit your `.env` file, database passwords, secret keys, or production credentials to Git.

### 5. Apply database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create an administrator account

```bash
python manage.py createsuperuser
```

### 7. Start the development server

```bash
python manage.py runserver
```

The local API will be available at:

`http://127.0.0.1:8000/`

The Django administration panel is available at:

`http://127.0.0.1:8000/admin/`

## API Endpoints

Base URL:

`http://127.0.0.1:8000/api/v1/`

### 1. Cars API

Base path: `/api/v1/cars/`

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| GET | `/api/v1/cars/car/` | List publicly available cars | Not required |
| POST | `/api/v1/cars/car/` | Submit a new car listing | Required |
| GET | `/api/v1/cars/<id>/` | Retrieve a car's details | Depends on view permissions |
| GET | `/api/v1/cars/car/` | List the authenticated owner's cars | Required |

**Important:** The public car listing and owner car listing currently share the same URL path, `/api/v1/cars/car/`. This can cause a route conflict. Give the owner endpoint a separate path, such as `/api/v1/cars/my-cars/`, to distinguish the two operations.

New car listings are intended to start with a pending status until approved.

### 2. User API

Base path: `/api/v1/user/`

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| POST | `/api/v1/user/login/` | Obtain JWT access and refresh tokens | Not required |
| POST | `/api/v1/user/signup/` | Register a new account | Not required |
| GET | `/api/v1/user/profile/` | Retrieve the authenticated user's profile | Required |
| GET | `/api/v1/user/refunded/` | Retrieve the authenticated user's refund records | Required |
| POST | `/api/v1/user/rechareg/` | Submit a balance recharge request | Depends on view permissions |

**Note:** The recharge route is spelled `rechareg` in the current URL configuration. Consider renaming it to `recharge` for clarity and consistency.

### 3. Bookings API

Base path: `/api/v1/books/`

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| GET | `/api/v1/books/car/` | List the authenticated user's bookings | Required |
| POST | `/api/v1/books/car/` | Create a car booking | Required |
| PATCH | `/api/v1/books/<id>/status/` | Update a booking's status | Required; car owner only |
| GET | `/api/v1/books/dashboard/` | Retrieve the owner's rental dashboard | Required |

Booking status values:

- `pending`
- `confirmed`
- `cancelled`
- `completed`

Bookings should validate rental dates, car availability, and conflicting reservations. The backend should calculate rental prices rather than trust totals submitted by the client.

## Authentication

The login endpoint uses JSON Web Tokens (JWT).

After a successful login, use the access token to call protected endpoints:

```http
Authorization: Bearer <your-access-token>
```

Send credentials and other request data as JSON where applicable:

```http
Content-Type: application/json
```

Keep access and refresh tokens secure. Never expose secret keys or private credentials in frontend source code.

## Permissions and Access Control

- Public users can access publicly available car listings.
- Authenticated users can create bookings and access their own protected resources.
- Car owners can manage booking statuses for bookings associated with their cars.
- User-specific endpoints should filter records by the authenticated user.
- Administrative actions should be protected by appropriate permissions.

Always enforce authorization on the backend; hiding a button in the frontend is not sufficient security.

## Error Handling

The API may return standard HTTP status codes, including:

| Status | Meaning |
|---|---|
| `200 OK` | Request completed successfully |
| `201 Created` | Resource created successfully |
| `400 Bad Request` | Invalid input or validation error |
| `401 Unauthorized` | Missing or invalid authentication |
| `403 Forbidden` | Authenticated user lacks permission |
| `404 Not Found` | Requested resource or route does not exist |
| `429 Too Many Requests` | Request rate limit exceeded |
| `500 Internal Server Error` | Unexpected server-side error |

## Development Guidelines

- Validate input with DRF serializers.
- Use permissions and queryset filtering to protect user data.
- Use database transactions for operations that update balances or consume recharge codes.
- Prevent duplicate or overlapping bookings.
- Store credentials in environment variables.
- Test authentication, permissions, validation, and business rules before deployment.
- Use HTTPS and disable Django debug mode in production.

## License

Add your chosen license before distributing this project publicly.