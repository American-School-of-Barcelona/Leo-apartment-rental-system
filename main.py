from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database setup
db_path = os.path.join(os.path.dirname(__file__), 'instance', 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# --- Define Tables (same as your schema.sql) ---
class Apartment(db.Model):
    apartment_number = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    max_guests = db.Column(db.Integer)

    bookings = db.relationship('Booking', backref='apartment', lazy=True)


class Booking(db.Model):
    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    apartment_number = db.Column(db.String, db.ForeignKey('apartment.apartment_number'), nullable=False)
    guest_name = db.Column(db.String, nullable=False)
    check_in_date = db.Column(db.String, nullable=False)
    check_out_date = db.Column(db.String, nullable=False)
    check_in_time = db.Column(db.String)
    check_out_time = db.Column(db.String)
    num_guests = db.Column(db.Integer)


# --- Create the database if it doesn't exist ---
with app.app_context():
    if not os.path.exists(db_path):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        db.create_all()


# --- Test route: Add a booking ---
@app.route("/add_test_booking")
def add_test_booking():
    test_booking = Booking(
        apartment_number="A1",
        guest_name="John Smith",
        check_in_date="2025-12-20",
        check_out_date="2025-12-25",
        check_in_time="15:00",
        check_out_time="10:00",
        num_guests=2
    )
    db.session.add(test_booking)
    db.session.commit()
    return "✅ Booking added successfully!"


# --- Test route: Show all bookings ---
@app.route("/show_bookings")
def show_bookings():
    all_bookings = Booking.query.all()
    output = "<h2>All Bookings:</h2><ul>"
    for b in all_bookings:
        output += f"<li>{b.guest_name} - {b.apartment_number} ({b.check_in_date} → {b.check_out_date})</li>"
    output += "</ul>"
    return output


if __name__ == "__main__":
    app.run(debug=True)
