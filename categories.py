from abc import ABC, abstractmethod

# Abstract Booking Category
class BookingCategory(ABC):
    def __init__(self, category_name, range_start, range_end):
        self._category_name = category_name
        self._seat_range_start = range_start
        self._seat_range_end = range_end
    
    @abstractmethod
    def get_price_multiplier(self):
        pass
    
    @abstractmethod
    def display_benefits(self):
        pass
    
    def get_category_name(self):
        return self._category_name
    
    def get_seat_range_start(self):
        return self._seat_range_start
    
    def get_seat_range_end(self):
        return self._seat_range_end

# First Class (F1-F10)
class FirstClass(BookingCategory):
    def __init__(self):
        super().__init__("First Class", 1, 10)
    
    def get_price_multiplier(self):
        return 3.0
    
    def display_benefits(self):
        return "Premium seats, Gourmet meals, Priority boarding, Extra baggage"

# Business Class (B11-B30)
class Business(BookingCategory):
    def __init__(self):
        super().__init__("Business", 11, 30)
    
    def get_price_multiplier(self):
        return 2.0
    
    def display_benefits(self):
        return "Comfortable seats, Meals included, Priority check-in"

# Economy Class (E31-E60)
class Economy(BookingCategory):
    def __init__(self):
        super().__init__("Economy", 31, 60)
    
    def get_price_multiplier(self):
        return 1.0
    
    def display_benefits(self):
        return "Standard seats, Snacks available"
