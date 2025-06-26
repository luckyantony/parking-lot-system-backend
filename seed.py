from dotenv import load_dotenv
load_dotenv()

from app import create_app
from extensions import db
from models import User, ParkingLot, ParkingSpot
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    try:
        # Only drop tables for local SQLite
        if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite"):
            db.drop_all()
        db.create_all()

        # Check for existing data to avoid duplicates
        if not User.query.filter_by(username="admin").first():
            admin = User(
                username="admin",
                email="admin@example.com",
                password_hash=generate_password_hash("adminpass")
            )
            db.session.add(admin)

        if not ParkingLot.query.filter_by(name="Lot A").first():
            lot = ParkingLot(name="Lot A", location="Nairobi CBD")
            db.session.add(lot)
            db.session.commit()

            for i in range(1, 11):
                spot = ParkingSpot(spot_number=f"A{i}", lot_id=lot.id)
                db.session.add(spot)

        db.session.commit()
        print("Seeded database successfully :)")
    except Exception as e:
        print(f"Error seeding database: {str(e)}")
        db.session.rollback()