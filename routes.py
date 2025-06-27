from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User, Vehicle, ParkingLot, ParkingSpot, Ticket
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import re

api = Blueprint("api", __name__)

# === Auth ===
@api.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    if not all([username, email, password]):
        return {"error": "All fields are required"}, 400
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return {"error": "Invalid email format"}, 400
    if len(password) < 8:
        return {"error": "Password must be at least 8 characters"}, 400
    if User.query.filter_by(username=username).first():
        return {"error": "Username already taken"}, 400
    if User.query.filter_by(email=email).first():
        return {"error": "Email already taken"}, 400
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    token = create_access_token(identity=str(user.id))  
    return {"user": user.to_dict(), "token": token}, 201

@api.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return {"error": "Invalid email or password"}, 401
    token = create_access_token(identity=str(user.id))  
    return {"user": user.to_dict(), "token": token}, 200

@api.route("/me", methods=["GET"])
@jwt_required()
def me():
    uid = get_jwt_identity()  
    user = User.query.get(int(uid))  
    if not user:
        return {"error": "User not found"}, 404
    return user.to_dict()

# === Vehicles ===
@api.route("/vehicles", methods=["GET", "POST"])
@jwt_required()
def vehicles():
    uid = int(get_jwt_identity())  
    if request.method == "POST":
        data = request.get_json()
        plate_number = data.get("plate_number")
        vehicle_type = data.get("type")
        if not plate_number:
            return {"error": "Plate number is required"}, 400
        vehicle = Vehicle(plate_number=plate_number, type=vehicle_type, user_id=uid)
        db.session.add(vehicle)
        db.session.commit()
        return vehicle.to_dict(), 201
    vehicles = Vehicle.query.filter_by(user_id=uid).all()
    return jsonify([v.to_dict() for v in vehicles])

# === Parking Lots ===
@api.route("/parking-lots", methods=["GET", "POST"])
@jwt_required()
def parking_lots():
    if request.method == "POST":
        data = request.get_json()
        name = data.get("name")
        location = data.get("location")
        if not name or not location:
            return {"error": "Name and location are required"}, 400
        lot = ParkingLot(name=name, location=location)
        db.session.add(lot)
        db.session.commit()
        return {"message": "Parking lot created", "lot_id": lot.id}, 201
    lots = ParkingLot.query.all()
    return jsonify([
        {
            "id": lot.id,
            "name": lot.name,
            "location": lot.location,
            "spots": len(lot.spots)
        } for lot in lots
    ])

# === Parking Spots ===
@api.route("/spots", methods=["GET"])
def get_spots():
    spots = ParkingSpot.query.all()
    return jsonify([{
        "id": s.id,
        "spot_number": s.spot_number,
        "status": s.status,
        "lot": s.lot.name if s.lot else None
    } for s in spots])

# === Tickets ===
@api.route("/tickets", methods=["GET", "POST"])
@jwt_required()
def tickets():
    uid = int(get_jwt_identity())
    if request.method == "POST":
        data = request.get_json()
        vehicle_id = data.get("vehicle_id")
        spot_id = data.get("parking_spot_id")
        if not vehicle_id or not spot_id:
            return {"error": "Vehicle ID and parking spot ID are required"}, 400
        spot = ParkingSpot.query.get(spot_id)
        if not spot or spot.status != "available":
            return {"error": "Spot unavailable"}, 400
        vehicle = Vehicle.query.get(vehicle_id)
        if not vehicle or vehicle.user_id != uid:
            return {"error": "Vehicle not found or not owned by user"}, 400
        ticket = Ticket(
            vehicle_id=vehicle_id,
            spot_id=spot.id,
            check_in=datetime.now()
        )
        spot.status = "occupied"
        db.session.add(ticket)
        db.session.commit()
        return {"message": "Spot booked", "ticket_id": ticket.id}, 201
    tickets = Ticket.query.join(Vehicle).filter(Vehicle.user_id == uid).all()
    return jsonify([
        {
            "id": t.id,
            "vehicle_id": t.vehicle_id,
            "spot_id": t.spot_id,
            "check_in": t.check_in.isoformat(),
            "check_out": t.check_out.isoformat() if t.check_out else None
        } for t in tickets
    ])

# === Checkout ===
@api.route("/checkout/<int:ticket_id>", methods=["PATCH"])
@jwt_required()
def checkout(ticket_id):
    uid = int(get_jwt_identity())
    ticket = Ticket.query.get(ticket_id)
    if not ticket or ticket.check_out:
        return {"error": "Invalid ticket or already checked out"}, 400
    if ticket.vehicle.user_id != uid:
        return {"error": "Not authorized to check out this ticket"}, 403
    ticket.check_out = datetime.now()
    ticket.spot.status = "available"
    db.session.commit()
    return {"message": "Checked out", "ticket_id": ticket.id}