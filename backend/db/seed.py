from app import create_app, db
from models import User, Vehicle, ParkingLot, ParkingSpot

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    user = User(username="admin")
    db.session.add(user)

    lot = ParkingLot(name="Lot A", location="Nairobi CBD")
    db.session.add(lot)

    for i in range(1, 11):
        spot = ParkingSpot(spot_number=f"A{i}", lot=lot)
        db.session.add(spot)

    db.session.commit()
    print("Seeded database.")
