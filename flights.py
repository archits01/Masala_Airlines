from abc import ABC, abstractmethod

# Abstract Flight class
class Flight(ABC):
    def __init__(self, flight_number, origin, destination, distance, base_fare_per_km):
        self._flight_number = flight_number
        self._origin = origin
        self._destination = destination
        self._distance = distance
        self._base_fare_per_km = base_fare_per_km
        self._booked_seats = []
    
    @abstractmethod
    def calculate_fare(self):
        pass
    
    def get_flight_number(self):
        return self._flight_number
    
    def get_origin(self):
        return self._origin
    
    def get_destination(self):
        return self._destination
    
    def is_seat_available(self, seat_number):
        return seat_number not in self._booked_seats
    
    def book_seat(self, seat_number):
        self._booked_seats.append(seat_number)
    
    def display_details(self):
        pass

# Normal Flight
class NormalFlight(Flight):
    def calculate_fare(self):
        return self._distance * self._base_fare_per_km
    
    def display_details(self):
        print(f"Flight: {self._flight_number} | {self._origin} → {self._destination} | Distance: {self._distance}km | Type: Normal")

# Red-Eye Flight
class RedEyeFlight(Flight):
    DISCOUNT_RATE = 0.10
    
    def calculate_fare(self):
        return self._distance * self._base_fare_per_km * (1 - self.DISCOUNT_RATE)
    
    def display_details(self):
        print(f"Flight: {self._flight_number} | {self._origin} → {self._destination} | Distance: {self._distance}km | Type: Red-Eye (10% off)")
