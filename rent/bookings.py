from flask import render_template
from .db import Booking

def allBookings():
    bookings = Booking.query.all()
    return render_template('templates/booking.html', bookings=bookings)