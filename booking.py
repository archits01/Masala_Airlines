from categories import FirstClass, Business, Economy

# Booking class
class Booking:
    def __init__(self, booking_id, passenger_name, flight, category, seat_number):
        self._booking_id = booking_id
        self._passenger_name = passenger_name
        self._flight = flight
        self._category = category
        self._seat_number = seat_number
        self._ticket_cost = self.calculate_ticket_cost()
    
    def calculate_ticket_cost(self):
        return self._flight.calculate_fare() * self._category.get_price_multiplier()
    
    def get_booking_id(self):
        return self._booking_id
    
    def get_passenger_name(self):
        return self._passenger_name
    
    def get_flight(self):
        return self._flight
    
    def display_booking(self):
        print(f"\n{'='*60}")
        print(f"Booking ID: {self._booking_id}")
        print(f"Passenger: {self._passenger_name}")
        print(f"Flight: {self._flight.get_flight_number()} | {self._flight.get_origin()} → {self._flight.get_destination()}")
        print(f"Class: {self._category.get_category_name()}")
        print(f"Seat: {self._seat_number}")
        print(f"Ticket Cost: ₹{self._ticket_cost:.2f}")
        print(f"Benefits: {self._category.display_benefits()}")
        print(f"{'='*60}")

# Booking System
class BookingSystem:
    def __init__(self):
        self._flights = []
        self._bookings = []
        self._next_booking_id = 1
    
    def add_flight(self, flight):
        self._flights.append(flight)
    
    def view_flights(self):
        print(f"\n{'='*60}")
        print("✈️  MASALA AIRLINES - AVAILABLE FLIGHTS")
        print(f"{'='*60}")
        for flight in self._flights:
            flight.display_details()
        print(f"{'='*60}")
    
    def find_flight(self, flight_number):
        for flight in self._flights:
            if flight.get_flight_number() == flight_number:
                return flight
        return None
    
    def _find_available_seat(self, flight, category):
        prefix = category.get_category_name()[0]  # F, B, or E
        for i in range(category.get_seat_range_start(), category.get_seat_range_end() + 1):
            seat_number = f"{prefix}{i}"
            if flight.is_seat_available(seat_number):
                return seat_number
        return None
    
    def create_booking(self, passenger_name, flight_number, category_type, seat_number):
        flight = self.find_flight(flight_number)
        if not flight:
            print("❌ Flight not found!")
            return None
        
        # Create category object
        if category_type == "1":
            category = FirstClass()
        elif category_type == "2":
            category = Business()
        elif category_type == "3":
            category = Economy()
        else:
            print("❌ Invalid category!")
            return None
        
        # Book the seat
        flight.book_seat(seat_number)
        
        # Create booking
        booking = Booking(self._next_booking_id, passenger_name, flight, category, seat_number)
        self._bookings.append(booking)
        self._next_booking_id += 1
        
        print("\n✅ Booking successful!")
        booking.display_booking()
        return booking
    
    def view_bookings(self):
        if not self._bookings:
            print("\n📭 No bookings found.")
            return
        
        print(f"\n{'='*60}")
        print("📋 YOUR BOOKINGS")
        print(f"{'='*60}")
        for booking in self._bookings:
            booking.display_booking()
    
    def cancel_booking(self, booking_id):
        for booking in self._bookings:
            if booking.get_booking_id() == booking_id:
                self._bookings.remove(booking)
                print(f"\n✅ Booking #{booking_id} cancelled successfully!")
                return
        print(f"\n❌ Booking #{booking_id} not found!")
