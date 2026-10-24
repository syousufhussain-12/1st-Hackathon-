# booking.py
import data
from data import ROUTES, BOOKINGS, ISSUED_IDS
from functions import get_valid_string, get_valid_integer, format_currency

def generate_booking_id():
    """Generates a unique booking ID"""
    booking_id = f"B{data.NEXT_BOOKING_ID}"
    data.NEXT_BOOKING_ID += 1
    ISSUED_IDS.add(booking_id)
    return booking_id

def book_ticket():
    print("\n--- BOOK A TICKET ---")
    
    # 1. Collect details & validate
    name = get_valid_string("Enter passenger name: ")
    age = get_valid_integer("Enter passenger age: ")
    route_id = get_valid_string("Enter Route ID (e.g., R101): ").upper()
    
    # 2. Find route & check existence
    selected_route = None
    for route in ROUTES:
        if route["route_id"] == route_id:
            selected_route = route
            break
            
    if not selected_route:
        print("Error: Route not found. Returning to main menu.")
        return
        
    seats = get_valid_integer("Enter number of seats: ")
    
    # 3. Validate seat availability
    if seats > selected_route["available_seats"]:
        print(f"Error: Not enough seats available. Only {selected_route['available_seats']} left.")
        return
        
    # 4. Create Record & Calculate Fare
    total_fare = selected_route["ticket_price"] * seats
    booking_id = generate_booking_id()
    
    booking_record = {
        "booking_id": booking_id,
        "passenger_name": name,
        "passenger_age": age,
        "route_id": route_id,
        "seats": seats,
        "total_fare": total_fare,
        "status": "Confirmed"
    }
    
    # 5. Update Seats and Save Record (Only after all checks pass)
    selected_route["available_seats"] -= seats
    BOOKINGS.append(booking_record)
    
    # 6. Confirmation Message
    print("\nBooking confirmed!")
    print(f"Booking ID: {booking_id}")
    print(f"Passenger: {name}")
    print(f"Route: {route_id} ({selected_route['departure_city']} -> {selected_route['destination_city']})")
    print(f"Seats booked: {seats}")
    print(f"Fare per seat: {format_currency(selected_route['ticket_price'])}")
    print(f"Total fare: {format_currency(total_fare)}")
    print(f"Status: Confirmed")

def view_bookings():
    print("\n--- MY BOOKINGS ---")
    if not BOOKINGS:
        print("No bookings found.")
        return
        
    for index, booking in enumerate(BOOKINGS, start=1):
        print(f"{index}. ID: {booking['booking_id']} | Name: {booking['passenger_name']} | Route: {booking['route_id']} | Seats: {booking['seats']} | Fare: {format_currency(booking['total_fare'])} | Status: {booking['status']}")

def cancel_booking():
    print("\n--- CANCEL A BOOKING ---")
    booking_id = get_valid_string("Enter booking ID to cancel (e.g., B1001): ").upper()
    
    for booking in BOOKINGS:
        if booking["booking_id"] == booking_id:
            if booking["status"] == "Cancelled":
                print("Error: This booking is already cancelled.")
                return
                
            # Restore seats exactly once
            for route in ROUTES:
                if route["route_id"] == booking["route_id"]:
                    route["available_seats"] += booking["seats"]
                    print(f"\nBooking {booking_id} has been cancelled.")
                    print(f"Seats restored: {booking['seats']}")
                    print(f"Route {route['route_id']} available seats: {route['available_seats']}")
                    break
                    
            # Update status to Cancelled
            booking["status"] = "Cancelled"
            return
            
    # If loop completes without break/finding the ID
    print(f"Error: Booking ID {booking_id} not found.")