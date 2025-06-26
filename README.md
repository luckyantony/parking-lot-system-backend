#  Parking Lot System API

A Flask RESTful API for managing a parking lot system with PostgreSQL and JWT-based authentication.

##  Learning Goals

* Build a backend API using Flask
* Use PostgreSQL for persistent data storage
* Implement JWT-based authentication
* Enforce route-based access control
* Work with related models: `User`, `Vehicle`, `ParkingLot`, `ParkingSpot`, `Ticket`

##  Requirements

* Python 3.8+
* PostgreSQL (local or via Render)
* pip
* Git
* Postman (optional, for testing)
* Render account (for deployment)

##  Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/luckyantony/parking-lot-system-backend.git
cd parking-lot-system-backend
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Create Database (Local Option)

```sql
CREATE DATABASE parking_lot_db;
```

Alternatively, use SQLite for local development by adjusting `config.py`.

### 4. Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/parking_lot_db
JWT_SECRET_KEY=your_secure_jwt_secret_key
FLASK_APP=app.py
```

Replace `your_password` with your PostgreSQL password. Generate a secure `JWT_SECRET_KEY` using `openssl rand -hex 32`.

### 5. Run Migrations & Seed Data

```bash
export FLASK_APP=app.py
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
python seed.py
```

### 6. Start the Server

```bash
flask run
# or
gunicorn app:app
```

Visit: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

Deployed: [https://parking-lot-system-3g7g.onrender.com/](https://parking-lot-system-3g7g.onrender.com/)

##  Auth Flow

### Register

```http
POST /api/register
Content-Type: application/json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}
```

### Login

```http
POST /api/login
Content-Type: application/json
{
  "email": "test@example.com",
  "password": "password123"
}
```

### Protected Routes Header

```
Authorization: Bearer <your_jwt_token>
```

##  API Endpoints

| Endpoint                    | Method | Auth Required | Description                         |
| --------------------------- | ------ | ------------- | ----------------------------------- |
| /api/register               | POST   | No            | Register a new user                 |
| /api/login                  | POST   | No            | Log in and get JWT token            |
| /api/me                     | GET    | Yes           | Get authenticated user details      |
| /api/vehicles               | GET    | Yes           | List user’s vehicles                |
| /api/vehicles               | POST   | Yes           | Register a new vehicle              |
| /api/parking-lots           | GET    | Yes           | List all parking lots               |
| /api/parking-lots           | POST   | Yes           | Create a new parking lot            |
| /api/spots                  | GET    | No            | List all parking spots              |
| /api/tickets                | POST   | Yes           | Book a parking spot (create ticket) |
| /api/checkout/\<ticket\_id> | PATCH  | Yes           | Check out a ticket                  |
| /api/test-db                | GET    | No            | Test database connectivity          |

##  Detailed Endpoints

### Register

```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

### Login

```json
{
  "email": "string",
  "password": "string"
}
```

### Get User

```json
{
  "id": integer,
  "username": "string",
  "email": "string"
}
```

### List Vehicles

```json
[
  {
    "id": integer,
    "plate_number": "string",
    "type": "string",
    "user_id": integer
  }
]
```

### Register Vehicle

```json
{
  "plate_number": "string",
  "type": "string"
}
```

### List Parking Lots

```json
[
  {
    "id": integer,
    "name": "string",
    "location": "string",
    "spots": integer
  }
]
```

### Create Parking Lot

```json
{
  "name": "string",
  "location": "string"
}
```

### List Parking Spots

```json
[
  {
    "id": integer,
    "spot_number": "string",
    "status": "available|occupied",
    "lot": "string"
  }
]
```

### Create Ticket

```json
{
  "vehicle_id": integer,
  "parking_spot_id": integer
}
```

### Checkout Ticket

```json
{
  "message": "Checked out",
  "ticket_id": integer
}
```

### Test DB

```python
@api.route("/test-db", methods=["GET"])
def test_db():
    try:
        db.session.execute("SELECT 1")
        return {"message": "Database connection successful"}
    except Exception as e:
        return {"error": f"Database connection failed: {str(e)}"}, 500
```

##  Data Models

* **User**: Unique username, email, hashed password
* **Vehicle**: Belongs to User, has plate number and optional type
* **ParkingLot**: Has name and location
* **ParkingSpot**: Belongs to ParkingLot, has spot number and status
* **Ticket**: Links Vehicle and ParkingSpot with check-in/out times

### Validations

* User: username/email unique, password ≥ 8 characters
* Vehicle: plate number required
* ParkingLot: name/location required
* ParkingSpot: spot number required
* Ticket: vehicle ID, spot ID, and check-in required

##  Postman Testing

1. Import `Parking_Lot_API_Collection.json`
2. Register/Login to get JWT token
3. Set `jwt_token` variable
4. Use token for protected routes

##  Tech Stack

* Python
* Flask
* PostgreSQL
* SQLAlchemy
* Flask-Migrate
* Flask-JWT-Extended
* Flask-CORS
* Gunicorn
* Render

##  Deployment (Render)

1. Push to GitHub
2. Create Web Service on Render
3. Set ENV variables:

   * `FLASK_APP=app.py`
   * `PYTHONUNBUFFERED=1`
   * `DATABASE_URL`
   * `JWT_SECRET_KEY`
4. Add `Procfile`:

```Procfile
release: flask db upgrade
web: gunicorn app:app
```

##  Author

Built by Luckyantony Leshan with 💻, ❤️, and ☕️

##  License

ISC License
