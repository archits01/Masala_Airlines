from booking import BookingSystem
from flights import NormalFlight, RedEyeFlight
from ui import ConsoleUI

def main():
    # Create booking system
    system = BookingSystem()
    
    # Hardcode 20 flights (10 Normal, 10 Red-Eye) - Diverse routes
    # Normal Flights
    system.add_flight(NormalFlight("SJ101", "Mumbai", "Delhi", 1150, 3.5))
    system.add_flight(NormalFlight("SJ102", "Delhi", "Kolkata", 1300, 3.0))
    system.add_flight(NormalFlight("SJ103", "Kolkata", "Chennai", 1600, 3.2))
    system.add_flight(NormalFlight("SJ104", "Chennai", "Bengaluru", 350, 2.8))
    system.add_flight(NormalFlight("SJ105", "Bengaluru", "Hyderabad", 500, 3.0))
    system.add_flight(NormalFlight("SJ106", "Hyderabad", "Goa", 600, 3.5))
    system.add_flight(NormalFlight("SJ107", "Goa", "Pune", 400, 2.9))
    system.add_flight(NormalFlight("SJ108", "Pune", "Jaipur", 1100, 3.1))
    system.add_flight(NormalFlight("SJ109", "Jaipur", "Ahmedabad", 650, 3.0))
    system.add_flight(NormalFlight("SJ110", "Ahmedabad", "Kochi", 1200, 3.3))
    
    # Red-Eye Flights
    system.add_flight(RedEyeFlight("SJ201", "Kochi", "Mumbai", 850, 3.5))
    system.add_flight(RedEyeFlight("SJ202", "Mumbai", "Delhi", 1150, 3.0))
    system.add_flight(RedEyeFlight("SJ203", "Delhi", "Kolkata", 1300, 3.2))
    system.add_flight(RedEyeFlight("SJ204", "Kolkata", "Chennai", 1600, 2.8))
    system.add_flight(RedEyeFlight("SJ205", "Chennai", "Bengaluru", 350, 3.0))
    system.add_flight(RedEyeFlight("SJ206", "Bengaluru", "Hyderabad", 500, 3.5))
    system.add_flight(RedEyeFlight("SJ207", "Hyderabad", "Goa", 600, 2.9))
    system.add_flight(RedEyeFlight("SJ208", "Goa", "Pune", 400, 3.1))
    system.add_flight(RedEyeFlight("SJ209", "Pune", "Jaipur", 1100, 3.0))
    system.add_flight(RedEyeFlight("SJ210", "Jaipur", "Ahmedabad", 650, 3.3))
    
    # Start UI
    ui = ConsoleUI(system)
    ui.start()

if __name__ == "__main__":
    main()
