# 🧘‍♂️ Fitness Class Booking API (Django + DRF)

This is a RESTful API built using **Django** and **Django REST Framework** that allows users to:

- View scheduled and cancelled fitness classes
- Book available classes
- Cancel individual bookings
- Cancel entire classes (admin/instructor)
- Handle timezone-aware scheduling

---

## 🚀 Features

- List all scheduled or cancelled classes with optional timezone conversion
- Book a class with automatic slot tracking
- Cancel bookings (client side)
- Cancel classes with automatic cascading booking cancellations (instructor/studio side)
- Admin dashboard for managing classes and bookings
- Timezone support with `?tz=` query parameter
- Filter by status using `?status=scheduled` or `cancelled`

---

## 🔗 API Endpoints

### 📚 Class Endpoints

| Method | Endpoint                                    | Description                             |
|--------|---------------------------------------------|-----------------------------------------|
| GET    | `/classes/`                                 | View all scheduled classes              |
| GET    | `/classes/?status=cancelled`                | View only cancelled classes             |
| GET    | `/classes/?tz=Asia/Kolkata`                 | Convert class times to given timezone   |
| POST   | `/create-class/`                            | Create a new class                      |
| POST   | `/cancel-class/<class_id>/`                 | Cancel a class (admin/instructor only)  |

---

### 🎟 Booking Endpoints

| Method | Endpoint                                         | Description                             |
|--------|--------------------------------------------------|-----------------------------------------|
| POST   | `/book/`                                         | Book a fitness class                    |
| GET    | `/bookings/?email=client@gmail.com`              | View all bookings by email              |
| POST   | `/cancel-booking/<booking_id>/`                  | Cancel a booking (client side)          |
| GET    | `/all-bookings/`                                 | View all bookings                       |
| GET    | `/all-bookings/?status=cancelled`                | Filter bookings by status               |

---

### ✅ Book a Class
```json
POST /book/
{
  "client_name": "John",
  "client_email": "john@gmail.com",
  "fitness_class": 1
}
```
### ✅ Create a Class
POST /create-class/
```
{
  "name": "HIIT",
  "date_time": "2025-07-07T10:00:00Z",
  "instructor": "Sofia",
  "total_slots": 20,
  "available_slots": 20,
  "status": "scheduled"
}
```

### Admin Panel
```
http://127.0.0.1:8000/admin/
```
Use your superuser credentials to:
- Create, update or delete classes
- Manually manage bookings

### Timezone Support
You can pass a timezone using the tz query parameter on /classes/:
``` GET /classes/?tz=Asia/Kolkata ```
Class times will be returned in the requested timezone using Python's pytz.

### Setup Instructions

1. Clone the repository
```
git clone https://github.com/mhdasif123/fitness-booking-api.git
cd fitness-booking-api
```
2. Create and activate a virtual environment
```
python -m venv venv
venv\Scripts\activate     # Windows
# or
source venv/bin/activate  # macOS/Linux
```
3. Install dependencies
```
pip install -r requirements.txt
```
4. Run migrations
```
python manage.py migrate
```
5. Create superuser (admin)
```
python manage.py createsuperuser
```
6. Start the server
```
python manage.py runserver
```

### Tech Stack
1. Python 3.x
2. Django
3. Django REST Framework
4. SQLite (for development)
5. Postman (for API testing)
