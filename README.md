Parking Lot System API
A Flask RESTful API for managing a parking lot system with PostgreSQL and JWT-based authentication.

🚀 Learning Goals

Build a Flask API backend
Use PostgreSQL for persistent data storage
Implement JWT-based authentication
Provide route-based access control
Work with multiple models: User, Vehicle, ParkingLot, ParkingSpot, Ticket


🫠 Requirements

Python 3.8+
PostgreSQL (installed locally or provisioned on Render)
pip (for dependency installation)
Postman account (optional for testing API endpoints)
Git (for cloning and managing the repository)
Render account (for deployment)


📦 Setup Instructions
1. Clone Repository
Clone the backend repository to your local machine:
git clone https://github.com/luckyantony/parking-lot-system-backend.git
cd parking-lot-system-backend

2. Install Dependencies
Install the required Python packages:
pip install -r requirements.txt

3. Create Local Database (Optional for Local Development)
If running locally, create a PostgreSQL database:
CREATE DATABASE parking_lot_db;

Alternatively, use SQLite for local development (configured in config.py).
4. Set Up Environment Variables
Create a .env file in the root directory with the following:
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/parking_lot_db
JWT_SECRET_KEY=your_secure_jwt_secret_key
FLASK_APP=app.py


Replace your_password with your PostgreSQL password.
Generate a secure JWT_SECRET_KEY (e.g., openssl rand -hex 32).
For Render, set DATABASE_URL and JWT_SECRET_KEY in the Render dashboard under Environment Variables.

5. Run Migrations and Seed Data
Initialize and apply database migrations:
export FLASK_APP=app.py
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

Seed the database with sample data (optional):
python seed.py

This creates an admin user (admin, admin@example.com, adminpass) and a sample parking lot with spots.
6. Start the Server
Run the Flask development server locally:
flask run

Or use Gunicorn for production-like testing:
gunicorn app:app

Visit: http://127.0.0.1:5000/
For the deployed app, visit: https://parking-lot-system-3g7g.onrender.com/

👩‍🔧 Auth Flow
Register
Register a new user to obtain a JWT token:
POST https://parking-lot-system-3g7g.onrender.com/api/register
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}

Response:
{
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  },
  "token": "your_jwt_token"
}

Login
Log in to retrieve a JWT token:
POST https://parking-lot-system-3g7g.onrender.com/api/login
Content-Type: application/json

{
  "email": "test@example.com",
  "password": "password123"
}

Response:
{
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  },
  "token": "your_jwt_token"
}

Protected Routes
For endpoints requiring authentication, include the JWT token in the header:
Authorization: Bearer your_jwt_token


📊 API Endpoints



Endpoint
Method
Auth Required
Description



/api/register
POST
No
Register a new user


/api/login
POST
No
Log in and get JWT token


/api/me
GET
Yes
Get authenticated user’s details


/api/vehicles
GET
Yes
List user’s vehicles


/api/vehicles
POST
Yes
Register a new vehicle


/api/parking-lots
GET
Yes
List all parking lots


/api/parking-lots
POST
Yes
Create a new parking lot


/api/spots
GET
No
List all parking spots


/api/tickets
POST
Yes
Book a parking spot (create ticket)


/api/checkout/<ticket_id>
PATCH
Yes
Check out a ticket


/api/test-db
GET
No
Test database connectivity


Detailed Endpoint Information

Register (/api/register)

Request:{
  "username": "string",
  "email": "string",
  "password": "string" // Min 8 characters
}


Response (201):{
  "user": { "id": integer, "username": "string", "email": "string" },
  "token": "string"
}


Errors (400): All fields are required, Invalid email format, Password must be at least 8 characters, Username already taken, Email already taken


Login (/api/login)

Request:{
  "email": "string",
  "password": "string"
}


Response (200):{
  "user": { "id": integer, "username": "string", "email": "string" },
  "token": "string"
}


Errors (401): Invalid email or password


Get Current User (/api/me)

Response (200):{
  "id": integer,
  "username": "string",
  "email": "string"
}


Errors (401, 404): Missing Authorization Header, Invalid token, User not found


List Vehicles (/api/vehicles)

Response (200):[
  {
    "id": integer,
    "plate_number": "string",
    "type": "string",
    "user_id": integer
  }
]




Register Vehicle (/api/vehicles)

Request:{
  "plate_number": "string",
  "type": "string" // Optional
}


Response (201):{
  "id": integer,
  "plate_number": "string",
  "type": "string",
  "user_id": integer
}


Errors (400): Plate number is required


List Parking Lots (/api/parking-lots)

Response (200):[
  {
    "id": integer,
    "name": "string",
    "location": "string",
    "spots": integer
  }
]




Create Parking Lot (/api/parking-lots)

Request:{
  "name": "string",
  "location": "string"
}


Response (201):{
  "message": "Parking lot created",
  "lot_id": integer
}


Errors (400): Name and location are required


List Parking Spots (/api/spots)

Response (200):[
  {
    "id": integer,
    "spot_number": "string",
    "status": "available|occupied",
    "lot": "string"
  }
]




Create Ticket (/api/tickets)

Request:{
  "vehicle_id": integer,
  "parking_spot_id": integer
}


Response (201):{
  "message": "Spot booked",
  "ticket_id": integer
}


Errors (400): Vehicle ID and parking spot ID are required, Spot unavailable, Vehicle not found


Checkout Ticket (/api/checkout/<ticket_id>)

Response (200):{
  "message": "Checked out",
  "ticket_id": integer
}


Errors (400): Invalid ticket or already checked out


Test Database (/api/test-db)

Note: Add this endpoint to routes.py for debugging:@api.route("/test-db", methods=["GET"])
def test_db():
    try:
        db.session.execute("SELECT 1")
        return {"message": "Database connection successful"}
    except Exception as e:
        return {"error": f"Database connection failed: {str(e)}"}, 500


Response (200):{
  "message": "Database connection successful"
}


Errors (500): Database connection failed: ...




📊 Data Models

User: Represents a user with a unique username, email, and password (hashed).
Vehicle: Belongs to a User, with a plate number and optional type (e.g., "SUV").
ParkingLot: Represents a parking lot with a name and location.
ParkingSpot: Belongs to a ParkingLot, with a spot number and status (available/occupied).
Ticket: Links a Vehicle and ParkingSpot, with check-in and check-out timestamps.

Validations

User: Username and email must be unique; password must be at least 8 characters.
Vehicle: Plate number is required.
ParkingLot: Name and location are required.
ParkingSpot: Spot number is required; status defaults to "available".
Ticket: Vehicle ID and parking spot ID are required; check-in is required, check-out is optional.


📂 Postman Testing

Open Postman.
Import the collection file Parking_Lot_API_Collection.json.
Set the jwt_token variable after running:
POST /api/register to create a user.
POST /api/login to retrieve a JWT token.


Use the token in the Authorization header (Bearer {{jwt_token}}) for protected endpoints:
/api/me, /api/vehicles, /api/parking-lots, /api/tickets, /api/checkout/<ticket_id>.


Test /api/test-db to verify database connectivity.


📈 Tech Stack

Python
Flask
PostgreSQL
SQLAlchemy
Flask-Migrate
Flask-JWT-Extended
Flask-CORS
Gunicorn (for production)
Render (for deployment)


🚀 Deployment on Render
The API is deployed on Render at https://parking-lot-system-3g7g.onrender.com.
Deployment Steps

Push the repository to GitHub: git push origin main.
Create a new Web Service on Render, linking to github.com/luckyantony/parking-lot-system-backend.
Set environment variables in Render’s dashboard:
FLASK_APP=app.py
PYTHONUNBUFFERED=1
DATABASE_URL (provided by Render’s PostgreSQL instance)
JWT_SECRET_KEY (secure random string)


Ensure Procfile and render.yaml are configured:
Procfile: release: flask db upgrade and web: gunicorn app:app
render.yaml: Defines build and release commands.


Deploy and monitor logs for errors.


👨‍💼 Author
Built with 💻, ❤️, and ☕ by Luckyantony Leshan

📄 License
ISC License