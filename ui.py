from categories import FirstClass, Business, Economy

# Console UI
class ConsoleUI:
    def __init__(self, booking_system):
        self._booking_system = booking_system
    
    def display_menu(self):
        print("\n" + "="*60)
        print("✈️  MASALA AIRLINES - AIRLINE TICKET BOOKING SYSTEM")
        print("="*60)
        print("1. View All Flights")
        print("2. View Flight Details")
        print("3. Make a New Booking")
        print("4. View My Bookings")
        print("5. Cancel a Booking")
        print("6. Exit")
        print("="*60)
    
    def handle_view_flights(self):
        self._booking_system.view_flights()
    
    def handle_flight_details(self):
        if not self._booking_system._flights:
            print("\n❌ No flights available!")
            return
            
        # Show available flights with numbers
        print(f"\n{'='*60}")
        print("Select Flight for Details:")
        print(f"{'='*60}")
        for i, flight in enumerate(self._booking_system._flights, 1):
            print(f"{i}. {flight.get_flight_number()} - {flight.get_origin()} → {flight.get_destination()}")
        print(f"{'='*60}")
        
        try:
            choice = int(input(f"\nSelect Flight (1-{len(self._booking_system._flights)}): "))
            if choice < 1 or choice > len(self._booking_system._flights):
                print("❌ Invalid choice!")
                return
            selected_flight = self._booking_system._flights[choice - 1]
            
            print(f"\n{'='*60}")
            selected_flight.display_details()
            print(f"Base Fare: ₹{selected_flight.calculate_fare():.2f}")
            print(f"{'='*60}")
        except ValueError:
            print("❌ Invalid input!")
    
    def handle_book_ticket(self):
        passenger_name = input("\nEnter Passenger Name: ")
        
        # Get unique origins and destinations
        origins = sorted(list(set(flight.get_origin() for flight in self._booking_system._flights)))
        destinations = sorted(list(set(flight.get_destination() for flight in self._booking_system._flights)))
        
        # Show origins
        print(f"\n{'='*60}")
        print("Select Origin:")
        print(f"{'='*60}")
        for i, origin in enumerate(origins, 1):
            print(f"{i}. {origin}")
        print(f"{'='*60}")
        
        try:
            origin_choice = int(input(f"\nSelect Origin (1-{len(origins)}): "))
            if origin_choice < 1 or origin_choice > len(origins):
                print("❌ Invalid choice!")
                return
            origin = origins[origin_choice - 1]
        except ValueError:
            print("❌ Invalid input!")
            return
        
        # Show destinations
        print(f"\n{'='*60}")
        print("Select Destination:")
        print(f"{'='*60}")
        for i, destination in enumerate(destinations, 1):
            print(f"{i}. {destination}")
        print(f"{'='*60}")
        
        try:
            dest_choice = int(input(f"\nSelect Destination (1-{len(destinations)}): "))
            if dest_choice < 1 or dest_choice > len(destinations):
                print("❌ Invalid choice!")
                return
            destination = destinations[dest_choice - 1]
        except ValueError:
            print("❌ Invalid input!")
            return
        
        # Find flights from origin to destination
        available_flights = [f for f in self._booking_system._flights if f.get_origin() == origin and f.get_destination() == destination]
        
        if not available_flights:
            print(f"\n❌ No Flights from {origin} to {destination}")
            return
        
        # Show available flights with numbers
        print(f"\n{'='*60}")
        print(f"Flights from {origin} to {destination}:")
        print(f"{'='*60}")
        for i, flight in enumerate(available_flights, 1):
            print(f"{i}. ", end="")
            flight.display_details()
        print(f"{'='*60}")
        
        try:
            choice = int(input(f"\nSelect Flight (1-{len(available_flights)}): "))
            if choice < 1 or choice > len(available_flights):
                print("❌ Invalid choice!")
                return
            selected_flight = available_flights[choice - 1]
        except ValueError:
            print("❌ Invalid input!")
            return
        
        print("\nSelect Class:")
        print("1. First Class (₹₹₹) - F1 to F10")
        print("2. Business (₹₹) - B11 to B30")
        print("3. Economy (₹) - E31 to E60")
        category_type = input("Enter choice (1-3): ")
        
        # Create category to get available seats
        if category_type == "1":
            category = FirstClass()
        elif category_type == "2":
            category = Business()
        elif category_type == "3":
            category = Economy()
        else:
            print("❌ Invalid category!")
            return
        
        # Show available seats
        prefix = category.get_category_name()[0]
        available_seats = []
        for i in range(category.get_seat_range_start(), category.get_seat_range_end() + 1):
            seat = f"{prefix}{i}"
            if selected_flight.is_seat_available(seat):
                available_seats.append(seat)
        
        if not available_seats:
            print(f"\n❌ No seats available in {category.get_category_name()}!")
            return
        
        print(f"\n{'='*60}")
        print(f"Available Seats in {category.get_category_name()}:")
        print(f"{'='*60}")
        for i, seat in enumerate(available_seats, 1):
            print(f"{i}. {seat}", end="  ")
            if i % 10 == 0:
                print()
        print(f"\n{'='*60}")
        
        try:
            seat_choice = int(input(f"\nSelect Seat (1-{len(available_seats)}): "))
            if seat_choice < 1 or seat_choice > len(available_seats):
                print("❌ Invalid choice!")
                return
            selected_seat = available_seats[seat_choice - 1]
        except ValueError:
            print("❌ Invalid input!")
            return
        
        # Calculate and show final price
        final_price = selected_flight.calculate_fare() * category.get_price_multiplier()
        print(f"\n{'='*60}")
        print(f"Final Ticket Price: ₹{final_price:.2f}")
        print(f"Selected Seat: {selected_seat}")
        print(f"{'='*60}")
        
        # Ask for confirmation
        confirm = input("\nConfirm booking? (yes/no): ").lower()
        if confirm != "yes" and confirm != "y":
            print("\n❌ Booking cancelled!")
            return
        
        self._booking_system.create_booking(passenger_name, selected_flight.get_flight_number(), category_type, selected_seat)
    
    def handle_view_bookings(self):
        self._booking_system.view_bookings()
    
    def handle_cancel_booking(self):
        try:
            booking_id = int(input("\nEnter Booking ID to cancel: "))
            self._booking_system.cancel_booking(booking_id)
        except ValueError:
            print("❌ Invalid Booking ID!")
    
    def start(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-6): ")
            
            if choice == "1":
                self.handle_view_flights()
            elif choice == "2":
                self.handle_flight_details()
            elif choice == "3":
                self.handle_book_ticket()
            elif choice == "4":
                self.handle_view_bookings()
            elif choice == "5":
                self.handle_cancel_booking()
            elif choice == "6":
                print("\n✈️  Thank you for choosing MASALA AIRLINES! Have a safe flight!")
                break
            else:
                print("\n❌ Invalid choice! Please try again.")
