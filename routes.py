# routes.py
from data import ROUTES, SUPPORTED_CITIES

def view_available_routes():
    print("\n--- AVAILABLE BUS ROUTES ---")
    print(f"{'No.':<5} {'Route':<6} {'Journey':<30} {'Depart':<10} {'Fare':<10} {'Seats'}")
    print("-" * 75)
    
    for index, route in enumerate(ROUTES, start=1):
        if route["available_seats"] == 0:
            seats_display = "Fully Booked"
        else:
            seats_display = f"{route['available_seats']}/{route['total_seats']}"
            
        journey = f"{route['departure_city']} -> {route['destination_city']}"
        print(f"{index:<5} {route['route_id']:<6} {journey:<30} {route['departure_time']:<10} {route['ticket_price']:<10} {seats_display}")

def search_route():
    print("\n--- SEARCH FOR A ROUTE ---")
    search_term = input("Search by route ID or city (e.g., Hyderabad): ").strip().lower()
    
    found = False
    print("\nSearch Results:")
    for route in ROUTES:
        # Case-insensitive matching
        if (search_term == route["route_id"].lower() or 
            search_term in route["departure_city"].lower() or 
            search_term in route["destination_city"].lower()):
            
            print(f"{route['route_id']} | {route['departure_city']} -> {route['destination_city']} | Rs. {route['ticket_price']} | {route['available_seats']} seats available")
            found = True
            
            # PRD says: stop after a unique route ID match
            if search_term == route["route_id"].lower():
                break
    else:
        # for-else: executes if loop completes without break (i.e., if no route ID was exactly matched)
        if not found:
            print("No matching routes found. Please check your input.")

def route_schedule():
    print("\n--- ROUTE SCHEDULE BY DEPARTURE CITY ---")
    
    # Nested loops as required by PRD
    for city in SUPPORTED_CITIES:
        print(f"{city}")
        city_has_routes = False
        
        for route in ROUTES:
            if route["departure_city"] == city:
                print(f"    {route['route_id']} -> {route['destination_city']} | {route['departure_time']}")
                city_has_routes = True
                
        if not city_has_routes:
            print("    No scheduled departures.")