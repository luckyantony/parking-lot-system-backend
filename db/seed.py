# db/seed.py
import sys
from os.path import dirname, join, abspath

# Correct path adjustment (remove 'backend' from imports)
sys.path.insert(0, abspath(join(dirname(__file__), '..'))

from app import create_app, db
from models import User, Vehicle, ParkingLot, ParkingSpot  # Direct imports

app = create_app()

with app.app_context():
    try:
        # First create all tables
        db.create_all()
        
        # Then seed data
        user = User(username="admin")
        db.session.add(user)

        lot = ParkingLot(name="Lot A", location="Nairobi CBD")
        db.session.add(lot)

        for i in range(1, 11):
            spot = ParkingSpot(spot_number=f"A{i}", lot=lot)
            db.session.add(spot)

        db.session.commit()
        print("✅ Database seeded successfully!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.session.rollback()