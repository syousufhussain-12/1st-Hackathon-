# main.py
from routes import view_available_routes, search_route, route_schedule
from booking import book_ticket, view_bookings, cancel_booking
from reports import generate_report
from filehandler import export_report_to_file

def display_menu():
    print("\n==============================")
    print("  SMART BUS RESERVATION SYSTEM")
    print("==============================")
    print("1. View Available Routes")
    print("2. Search for a Route")
    print("3. Book a Ticket")
    print("4. View My Bookings")
    print("5. Cancel a Booking")
    print("6. View Seat Availability")
    print("7. Generate Booking Report")
    print("8. Route Schedule (Departure)")
    print("9. Export Report to File")
    print("10. Exit")
    print("==============================")

def view_seat_availability():
    print("\n--- SEAT AVAILABILITY ---")
    for route in __import__('data').ROUTES:
        status = "Fully Booked" if route["available_seats"] == 0 else f"{route['available_seats']} available"
        print(f"{route['route_id']}: {status} (Total Capacity: {route['total_seats']})")

def main():
    while True:
        display_menu()
        choice = input("Enter your choice (1-10): ").strip()
        
        if choice == '1':
            view_available_routes()
        elif choice == '2':
            search_route()
        elif choice == '3':
            book_ticket()
        elif choice == '4':
            view_bookings()
        elif choice == '5':
            cancel_booking()
        elif choice == '6':
            view_seat_availability()
        elif choice == '7':
            generate_report()
        elif choice == '8':
            route_schedule()
        elif choice == '9':
            export_report_to_file()
        elif choice == '10':
            print("Thank you for using Smart Bus Reservation System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 10.")

if __name__ == "__main__":
    main()