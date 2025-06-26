from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User, Vehicle, ParkingLot, ParkingSpot, Ticket
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

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

    if User.query.filter_by(username=username).first():
        return {"error": "Username already taken"}, 400
    if User.query.filter_by(email=email).first():
        return {"error": "Email already taken"}, 400

    hashed_pw = generate_password_hash(password)
    user = User(username=username, email=email, password_hash=hashed_pw)
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=user.id)
    return {"user": user.to_dict(), "token": token}, 201


@api.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return {"error": "Invalid email or password"}, 401

    token = create_access_token(identity=user.id)
    return {"user": user.to_dict(), "token": token}, 200


@api.route("/me", methods=["GET"])
@jwt_required()
def me():
    uid = get_jwt_identity()
    user = User.query.get(uid)
    return user.to_dict()

# === Vehicles ===

@api.route("/vehicles", methods=["GET", "POST"])
@jwt_required()
def vehicles():
    uid = get_jwt_identity()
    if request.method == "POST":
        data = request.json
        vehicle = Vehicle(plate_number=data["plate_number"], user_id=uid)
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

# === Book Spot ===

@api.route("/book", methods=["POST"])
@jwt_required()
def book_spot():
    data = request.json
    spot = ParkingSpot.query.get(data["spot_id"])
    if not spot or spot.status != "available":
        return {"error": "Spot unavailable"}, 400

    ticket = Ticket(
        vehicle_id=data["vehicle_id"],
        spot_id=spot.id,
        check_in=datetime.now().isoformat()
    )
    spot.status = "occupied"
    db.session.add(ticket)
    db.session.commit()
    return {"message": "Spot booked", "ticket_id": ticket.id}

# === Checkout ===

@api.route("/checkout/<int:ticket_id>", methods=["PATCH"])
@jwt_required()
def checkout(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if not ticket or ticket.check_out:
        return {"error": "Invalid ticket or already checked out"}, 400
    ticket.check_out = datetime.now().isoformat()
    ticket.spot.status = "available"
    db.session.commit()
    return {"message": "Checked out", "ticket_id": ticket.id}
