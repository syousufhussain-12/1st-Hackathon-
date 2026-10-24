import streamlit as st
import pandas as pd

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Smart Bus Reservation", page_icon="🚌", layout="wide")

# --- INITIAL DATA SETUP (Session State for In-Memory Storage) ---
if 'routes' not in st.session_state:
    st.session_state.routes = [
        {"route_id": "R101", "departure_city": "Karachi", "destination_city": "Hyderabad", "departure_time": "08:00 AM", "ticket_price": 1200, "total_seats": 40, "available_seats": 40},
        {"route_id": "R102", "departure_city": "Karachi", "destination_city": "Sukkur", "departure_time": "09:30 AM", "ticket_price": 2000, "total_seats": 36, "available_seats": 36},
        {"route_id": "R103", "departure_city": "Hyderabad", "destination_city": "Mirpur Khas", "departure_time": "11:00 AM", "ticket_price": 800, "total_seats": 32, "available_seats": 32},
        {"route_id": "R104", "departure_city": "Karachi", "destination_city": "Lahore", "departure_time": "07:00 PM", "ticket_price": 5000, "total_seats": 45, "available_seats": 45},
        {"route_id": "R105", "departure_city": "Sukkur", "destination_city": "Hyderabad", "departure_time": "02:00 PM", "ticket_price": 1500, "total_seats": 30, "available_seats": 30}
    ]

if 'bookings' not in st.session_state:
    st.session_state.bookings = []

if 'next_booking_id' not in st.session_state:
    st.session_state.next_booking_id = 1001

# --- SIDEBAR MENU ---
st.sidebar.title("🚌 Smart Bus System")
st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigation", [
    "View Routes", 
    "Search Route", 
    "Book Ticket", 
    "My Bookings", 
    "Cancel Booking",
    "View Seat Availability",
    "Reports & Schedule"
])

# --- MAIN APP ---
st.title("Ticket Booking & Reservation System")
st.markdown("---")

# 1. VIEW ROUTES
if menu == "View Routes":
    st.subheader("Available Bus Routes")
    df_routes = pd.DataFrame(st.session_state.routes)
    df_routes['Journey'] = df_routes['departure_city'] + " ➔ " + df_routes['destination_city']
    
    display_df = df_routes[['route_id', 'Journey', 'departure_time', 'ticket_price', 'available_seats', 'total_seats']]
    display_df.columns = ['Route ID', 'Journey', 'Departure Time', 'Fare (Rs)', 'Available Seats', 'Total Seats']
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# 2. SEARCH ROUTE
elif menu == "Search Route":
    st.subheader("Search for a Route")
    search_term = st.text_input("Enter Route ID or City name (e.g., R101, Karachi):").lower()
    
    if search_term:
        results = [r for r in st.session_state.routes if 
                   search_term in r['route_id'].lower() or 
                   search_term in r['departure_city'].lower() or 
                   search_term in r['destination_city'].lower()]
        
        if results:
            st.success(f"Found {len(results)} route(s)")
            st.dataframe(pd.DataFrame(results), use_container_width=True, hide_index=True)
        else:
            st.error("No matching routes found. Please try again.")

# 3. BOOK TICKET
elif menu == "Book Ticket":
    st.subheader("Book a New Ticket")
    
    with st.form("booking_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Passenger Name")
            age = st.number_input("Age", min_value=1, max_value=120, step=1)
        with col2:
            route_id = st.selectbox("Select Route", [r['route_id'] for r in st.session_state.routes])
            seats = st.number_input("Number of Seats", min_value=1, step=1)
            
        submit = st.form_submit_button("Confirm Booking", type="primary")
        
        if submit:
            if not name.strip():
                st.error("Passenger name cannot be empty.")
            else:
                selected_route = next((r for r in st.session_state.routes if r['route_id'] == route_id), None)
                
                if seats > selected_route['available_seats']:
                    st.error(f"Not enough seats! Only {selected_route['available_seats']} seats are available.")
                else:
                    # Create Booking Record
                    total_fare = selected_route['ticket_price'] * seats
                    booking_id = f"B{st.session_state.next_booking_id}"
                    st.session_state.next_booking_id += 1
                    
                    booking = {
                        "booking_id": booking_id,
                        "passenger_name": name,
                        "passenger_age": age,
                        "route_id": route_id,
                        "seats": seats,
                        "total_fare": total_fare,
                        "status": "Confirmed"
                    }
                    
                    # Update State
                    selected_route['available_seats'] -= seats
                    st.session_state.bookings.append(booking)
                    
                    st.success(f"Booking Confirmed! Your Booking ID is **{booking_id}**")
                    st.info(f"Total Fare to pay: Rs. {total_fare:,}")

# 4. MY BOOKINGS
elif menu == "My Bookings":
    st.subheader("Booking History")
    if not st.session_state.bookings:
        st.warning("No bookings found.")
    else:
        df_bookings = pd.DataFrame(st.session_state.bookings)
        # Formatting columns
        df_bookings = df_bookings[['booking_id', 'passenger_name', 'passenger_age', 'route_id', 'seats', 'total_fare', 'status']]
        df_bookings.columns = ['Booking ID', 'Passenger Name', 'Age', 'Route ID', 'Seats', 'Total Fare (Rs)', 'Status']
        
        st.dataframe(df_bookings, use_container_width=True, hide_index=True)

# 5. CANCEL BOOKING
elif menu == "Cancel Booking":
    st.subheader("Cancel a Booking")
    confirmed_bookings = [b['booking_id'] for b in st.session_state.bookings if b['status'] == 'Confirmed']
    
    if not confirmed_bookings:
        st.info("No confirmed bookings available to cancel.")
    else:
        cancel_id = st.selectbox("Select Booking ID to Cancel", confirmed_bookings)
        
        if st.button("Cancel Booking", type="primary"):
            for b in st.session_state.bookings:
                if b['booking_id'] == cancel_id:
                    b['status'] = 'Cancelled'
                    # Restore seats exactly once
                    for r in st.session_state.routes:
                        if r['route_id'] == b['route_id']:
                            r['available_seats'] += b['seats']
                            break
                    st.success(f"Booking {cancel_id} cancelled successfully. Seats restored.")
                    st.rerun()

# 6. VIEW SEAT AVAILABILITY
elif menu == "View Seat Availability":
    st.subheader("Seat Availability Status")
    st.write("Real-time seat availability across all routes.")
    
    availability_data = []
    for r in st.session_state.routes:
        if r['available_seats'] == r['total_seats']:
            status = "🟢 Fully Available"
        elif r['available_seats'] == 0:
            status = "🔴 Fully Booked"
        else:
            status = "🟡 Partially Booked"
            
        availability_data.append({
            "Route ID": r['route_id'],
            "Journey": f"{r['departure_city']} ➔ {r['destination_city']}",
            "Total Capacity": r['total_seats'],
            "Available Seats": r['available_seats'],
            "Status": status
        })
        
    df_availability = pd.DataFrame(availability_data)
    st.dataframe(df_availability, use_container_width=True, hide_index=True)

# 7. REPORTS & SCHEDULE
elif menu == "Reports & Schedule":
    st.subheader("Business Reports & Schedules")
    
    tab1, tab2 = st.tabs(["📊 Booking Report", "🕒 Route Schedule"])
    
    with tab1:
        total_created = len(st.session_state.bookings)
        confirmed = [b for b in st.session_state.bookings if b['status'] == 'Confirmed']
        cancelled = [b for b in st.session_state.bookings if b['status'] == 'Cancelled']
        revenue = sum(b['total_fare'] for b in confirmed)
        seats_reserved = sum(b['seats'] for b in confirmed)
        fully_booked = sum(1 for r in st.session_state.routes if r['available_seats'] == 0)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Bookings", total_created)
        col2.metric("Confirmed Bookings", len(confirmed))
        col3.metric("Cancelled Bookings", len(cancelled))
        
        st.markdown("---")
        
        col4, col5, col6 = st.columns(3)
        col4.metric("Seats Currently Reserved", seats_reserved)
        col5.metric("Confirmed Revenue", f"Rs. {revenue:,}")
        col6.metric("Fully Booked Routes", fully_booked)
        
    with tab2:
        st.write("### Departure Schedule by City")
        cities = ['Karachi', 'Hyderabad', 'Sukkur', 'Mirpur Khas', 'Lahore']
        for city in cities:
            city_routes = [r for r in st.session_state.routes if r['departure_city'] == city]
            with st.expander(f"📍 {city}"):
                if city_routes:
                    for cr in city_routes:
                        st.write(f"**{cr['route_id']}** ➔ {cr['destination_city']} | Departure: {cr['departure_time']} | Fare: Rs. {cr['ticket_price']}")
                else:
                    st.info("No scheduled departures from this city.")