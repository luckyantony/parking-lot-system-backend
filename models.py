from extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    vehicles = db.relationship("Vehicle", backref="user", cascade="all, delete")

    def to_dict(self):
        return {"id": self.id, "username": self.username}

class Vehicle(db.Model):
    __tablename__ = "vehicles"

    id = db.Column(db.Integer, primary_key=True)
    plate_number = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    tickets = db.relationship("Ticket", backref="vehicle", cascade="all, delete")

    def to_dict(self):
        return {
            "id": self.id,
            "plate_number": self.plate_number,
            "user_id": self.user_id
        }

class ParkingLot(db.Model):
    __tablename__ = "parking_lots"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String)
    spots = db.relationship("ParkingSpot", backref="lot", cascade="all, delete")

class ParkingSpot(db.Model):
    __tablename__ = "parking_spots"

    id = db.Column(db.Integer, primary_key=True)
    spot_number = db.Column(db.String, nullable=False)
    status = db.Column(db.String, default="available")  # available, occupied
    lot_id = db.Column(db.Integer, db.ForeignKey("parking_lots.id"))
    tickets = db.relationship("Ticket", backref="spot", cascade="all, delete")

class Ticket(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicles.id"))
    spot_id = db.Column(db.Integer, db.ForeignKey("parking_spots.id"))
    check_in = db.Column(db.String)
    check_out = db.Column(db.String)
