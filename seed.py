from app import create_app
from extensions import db
from models import User, ParkingLot, ParkingSpot

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    user = User(username="admin")
    db.session.add(user)

    lot = ParkingLot(name="Lot A", location="Nairobi CBD")
    db.session.add(lot)
    db.session.commit()

    for i in range(1, 11):
        spot = ParkingSpot(spot_number=f"A{i}", lot_id=lot.id)
        db.session.add(spot)

    db.session.commit()
    print(" Seeded database successfully:)!")
