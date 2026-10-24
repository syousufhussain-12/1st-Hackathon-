# reports.py
from data import ROUTES, BOOKINGS
from functions import format_currency

def generate_report():
    print("\n--- BOOKING REPORT ---")
    
    total_created = len(BOOKINGS)
    confirmed_count = 0
    cancelled_count = 0
    seats_reserved = 0
    confirmed_revenue = 0
    fully_booked = 0
    
    # Calculate Totals
    for booking in BOOKINGS:
        if booking["status"] == "Confirmed":
            confirmed_count += 1
            seats_reserved += booking["seats"]
            confirmed_revenue += booking["total_fare"]
        elif booking["status"] == "Cancelled":
            cancelled_count += 1
            
    # Count fully booked routes using nested loop approach (PRD requirement)
    for route in ROUTES:
        if route["available_seats"] == 0:
            fully_booked += 1
            
    print(f"Total bookings created: {total_created}")
    print(f"Confirmed bookings: {confirmed_count}")
    print(f"Cancelled bookings: {cancelled_count}")
    print(f"Seats currently reserved: {seats_reserved}")
    print(f"Confirmed revenue: {format_currency(confirmed_revenue)}")
    print(f"Fully booked routes: {fully_booked}")