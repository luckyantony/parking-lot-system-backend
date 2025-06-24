from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User, Vehicle, ParkingLot, ParkingSpot, Ticket
from datetime import datetime

api = Blueprint("api", __name__)

# === Auth Routes ===

@api.route("/register", methods=["POST"])
def register():
    data = request.json
    if User.query.filter_by(username=data["username"]).first():
        return {"error": "Username taken"}, 400
    user = User(username=data["username"])
    db.session.add(user)
    db.session.commit()
    token = create_access_token(identity=user.id)
    return {"user": user.to_dict(), "token": token}

@api.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()
    if user:
        token = create_access_token(identity=user.id)
        return {"user": user.to_dict(), "token": token}
    return {"error": "Invalid login"}, 401

@api.route("/me")
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

# === Parking Spots ===

@api.route("/spots", methods=["GET"])
def spots():
    spots = ParkingSpot.query.all()
    return jsonify([
        {
            "id": s.id,
            "spot_number": s.spot_number,
            "status": s.status,
            "lot": s.lot.name if s.lot else None
        } for s in spots
    ])

# === Book a Spot ===

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
        return {"error": "Already checked out or not found"}, 400
    ticket.check_out = datetime.now().isoformat()
    ticket.spot.status = "available"
    db.session.commit()
    return {"message": "Checked out", "ticket_id": ticket.id}
