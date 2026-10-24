# filehandler.py
from data import BOOKINGS, ROUTES

def export_report_to_file():
    """Optional feature: Saves the report to a text file (Professional touch)"""
    filename = "Booking_Report.txt"
    try:
        with open(filename, "w") as file:
            file.write("--- SMART BUS SYSTEM REPORT ---\n")
            file.write(f"Total Bookings: {len(BOOKINGS)}\n")
            
            file.write("\n--- Detailed Bookings ---\n")
            if not BOOKINGS:
                file.write("No bookings yet.\n")
            for b in BOOKINGS:
                file.write(f"{b['booking_id']} | {b['passenger_name']} | {b['route_id']} | {b['status']}\n")
                
            file.write("\n--- Routes Status ---\n")
            for r in ROUTES:
                file.write(f"{r['route_id']} | Seats Available: {r['available_seats']}/{r['total_seats']}\n")
                
        print(f"\n[Success] Report successfully exported to '{filename}' in the project folder!")
    except Exception as e:
        print(f"\n[Error] Could not export report: {e}")