# qt_ui.py

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem, QLineEdit,
    QComboBox, QGridLayout, QMessageBox, QDialog, QGroupBox, QInputDialog
)
from PyQt5.QtCore import Qt

# Import backend classes
# Note: Ensure categories.py and booking.py are in the same directory
from categories import FirstClass, Business, Economy
from booking import BookingSystem

class MasalaAirlinesApp(QMainWindow):
    """Main window for the Masala Airlines PyQt GUI."""
    def __init__(self, booking_system):
        super().__init__()
        self._booking_system = booking_system
        self.setWindowTitle("✈️ MASALA AIRLINES - Flight Booking System")
        self.setGeometry(100, 100, 800, 600)
        
        self._central_widget = QWidget()
        self.setCentralWidget(self._central_widget)
        
        self._layout = QVBoxLayout(self._central_widget)
        
        # Title
        self._title = QLabel("<h1>MASALA AIRLINES</h1>")
    # (Intentionally avoid setAlignment call to bypass static type issues with Qt enums)
        self._layout.addWidget(self._title)
        
        # Menu Buttons
        self._menu_group = QGroupBox("Main Menu")
        self._menu_layout = QVBoxLayout(self._menu_group)
        
        self._btn_view_flights = QPushButton("1. View All Flights")
        self._btn_view_flights.clicked.connect(self.view_all_flights)
        
        self._btn_book_ticket = QPushButton("2. Make a New Booking")
        self._btn_book_ticket.clicked.connect(self.show_book_ticket_dialog)

        self._btn_view_bookings = QPushButton("3. View My Bookings")
        self._btn_view_bookings.clicked.connect(self.view_my_bookings)
        
        self._btn_cancel_booking = QPushButton("4. Cancel a Booking")
        self._btn_cancel_booking.clicked.connect(self.show_cancel_booking_dialog)

        self._btn_exit = QPushButton("5. Exit")
        # Use a dedicated slot method for exiting (type-checker friendly)
        self._btn_exit.clicked.connect(self._exit_app)

        self._menu_layout.addWidget(self._btn_view_flights)
        self._menu_layout.addWidget(self._btn_book_ticket)
        self._menu_layout.addWidget(self._btn_view_bookings)
        self._menu_layout.addWidget(self._btn_cancel_booking)
        self._menu_layout.addWidget(self._btn_exit)
        
        self._layout.addWidget(self._menu_group)

        # Status Label
        self._status_label = QLabel("Welcome to Masala Airlines!")
        self._layout.addWidget(self._status_label)
        
        # Flight Table Widget (for dynamic display)
        self._flight_table = QTableWidget()
        self._flight_table.setColumnCount(5)
        self._flight_table.setHorizontalHeaderLabels(["Flight", "Route", "Distance (km)", "Type", "Base Fare (₹)"])
        self._flight_table.setHidden(True)
        self._layout.addWidget(self._flight_table)
        
        # Booking Table Widget
        self._booking_table = QTableWidget()
        self._booking_table.setColumnCount(5)
        self._booking_table.setHorizontalHeaderLabels(["ID", "Passenger", "Flight", "Seat & Class", "Cost (₹)"])
        self._booking_table.setHidden(True)
        self._layout.addWidget(self._booking_table)


    def _hide_all_content_widgets(self):
        """Hides tables when switching menu options."""
        self._flight_table.setHidden(True)
        self._booking_table.setHidden(True)

    def _exit_app(self):
        """Slot used for Exit button; separated out to satisfy static type checks."""
        self.close()
        return None
    
    # --- Menu 1: View All Flights ---
    def view_all_flights(self):
        self._hide_all_content_widgets()
        
        flights = self._booking_system._flights
        self._flight_table.setRowCount(len(flights))
        
        for row, flight in enumerate(flights):
            fare = flight.calculate_fare()
            flight_type = "Red-Eye (10% off)" if hasattr(flight, 'DISCOUNT_RATE') else "Normal"
            
            self._flight_table.setItem(row, 0, QTableWidgetItem(flight.get_flight_number()))
            self._flight_table.setItem(row, 1, QTableWidgetItem(f"{flight.get_origin()} → {flight.get_destination()}"))
            self._flight_table.setItem(row, 2, QTableWidgetItem(f"{flight._distance}"))
            self._flight_table.setItem(row, 3, QTableWidgetItem(flight_type))
            self._flight_table.setItem(row, 4, QTableWidgetItem(f"₹{fare:.2f}"))
            
        self._flight_table.resizeColumnsToContents()
        self._flight_table.setHidden(False)
        self._status_label.setText("Displaying all available flights.")

    # --- Menu 3: View My Bookings ---
    def view_my_bookings(self):
        self._hide_all_content_widgets()
        
        bookings = self._booking_system._bookings
        if not bookings:
            QMessageBox.information(self, "No Bookings", "No bookings found.")
            return

        self._booking_table.setRowCount(len(bookings))
        
        for row, booking in enumerate(bookings):
            flight_info = f"{booking._flight.get_flight_number()} ({booking._flight.get_origin()} → {booking._flight.get_destination()})"
            seat_class_info = f"{booking._seat_number} ({booking._category.get_category_name()})"
            
            self._booking_table.setItem(row, 0, QTableWidgetItem(str(booking.get_booking_id())))
            self._booking_table.setItem(row, 1, QTableWidgetItem(booking.get_passenger_name()))
            self._booking_table.setItem(row, 2, QTableWidgetItem(flight_info))
            self._booking_table.setItem(row, 3, QTableWidgetItem(seat_class_info))
            self._booking_table.setItem(row, 4, QTableWidgetItem(f"₹{booking._ticket_cost:.2f}"))
        
        self._booking_table.resizeColumnsToContents()
        self._booking_table.setHidden(False)
        self._status_label.setText(f"Displaying {len(bookings)} bookings.")

    # --- Menu 4: Cancel a Booking ---
    def show_cancel_booking_dialog(self):
        self._hide_all_content_widgets()
        booking_id, ok = QInputDialog.getInt(self, "Cancel Booking", "Enter Booking ID to cancel:", 0, 1, 9999)
        
        if ok and booking_id > 0:
            found = False
            for booking in self._booking_system._bookings:
                if booking.get_booking_id() == booking_id:
                    # Manually unbook the seat (since BookingSystem doesn't have a dedicated unbook method)
                    booking._flight._booked_seats.remove(booking._seat_number)
                    
                    self._booking_system._bookings.remove(booking)
                    QMessageBox.information(self, "Success", f"✅ Booking **#{booking_id}** cancelled successfully!")
                    self.view_my_bookings() # Refresh booking list
                    found = True
                    break
            
            if not found:
                QMessageBox.warning(self, "Error", f"❌ Booking **#{booking_id}** not found!")

    # --- Menu 2: Make a New Booking (Dialog) ---
    def show_book_ticket_dialog(self):
        self._hide_all_content_widgets()
        
        dialog = BookTicketDialog(self._booking_system, self)
        if dialog.exec_() == QDialog.Accepted:
            # If booking was successful, refresh the booking view automatically
            self.view_my_bookings()
            self._status_label.setText("New booking successfully created. See 'Your Bookings' tab.")
        else:
            self._status_label.setText("Booking cancelled or failed.")


class BookTicketDialog(QDialog):
    """A multi-step dialog for selecting route, flight, class, and seat."""
    def __init__(self, booking_system, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Book a New Ticket")
        self.setGeometry(200, 200, 600, 400)
        self._booking_system = booking_system
        self._selected_flight = None
        
        # Map category choice ('1', '2', '3') to class object
        self.flight_category_map = {
            "1": FirstClass,
            "2": Business,
            "3": Economy
        }

        self._layout = QVBoxLayout(self)

        # 1. Passenger Name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Passenger Name:"))
        self._name_input = QLineEdit()
        name_layout.addWidget(self._name_input)
        self._layout.addLayout(name_layout)

        # 2. Route Selection
        route_group = QGroupBox("1. Select Route")
        route_layout = QGridLayout(route_group)
        
        # Get unique origins and destinations from the system
        origins = sorted(list(set(f.get_origin() for f in self._booking_system._flights)))
        destinations = sorted(list(set(f.get_destination() for f in self._booking_system._flights)))

        self._origin_combo = QComboBox()
        self._origin_combo.addItem("— Select Origin —")
        self._origin_combo.addItems(origins)
        self._origin_combo.currentIndexChanged.connect(self.filter_flights)

        self._destination_combo = QComboBox()
        self._destination_combo.addItem("— Select Destination —")
        self._destination_combo.addItems(destinations)
        self._destination_combo.currentIndexChanged.connect(self.filter_flights)
        
        route_layout.addWidget(QLabel("Origin:"), 0, 0)
        route_layout.addWidget(self._origin_combo, 0, 1)
        route_layout.addWidget(QLabel("Destination:"), 1, 0)
        route_layout.addWidget(self._destination_combo, 1, 1)
        self._layout.addWidget(route_group)

        # 3. Flight Selection
        flight_group = QGroupBox("2. Select Flight")
        flight_layout = QVBoxLayout(flight_group)
        self._flight_list = QComboBox()
        self._flight_list.currentIndexChanged.connect(self.show_flight_details)
        flight_layout.addWidget(self._flight_list)
        self._flight_details_label = QLabel("Select a route to view flights.")
        flight_layout.addWidget(self._flight_details_label)
        self._layout.addWidget(flight_group)

        # 4. Class and Seat Selection
        booking_group = QGroupBox("3. Select Class and Seat")
        booking_layout = QGridLayout(booking_group)
        
        self._class_combo = QComboBox()
        self._class_combo.addItem("— Select Class —")
        self._class_combo.addItems(["1. First Class (3x)", "2. Business (2x)", "3. Economy (1x)"])
        self._class_combo.currentIndexChanged.connect(self.populate_seats)

        self._seat_combo = QComboBox()
        self._seat_combo.currentIndexChanged.connect(self.calculate_fare)
        
        booking_layout.addWidget(QLabel("Booking Class:"), 0, 0)
        booking_layout.addWidget(self._class_combo, 0, 1)
        booking_layout.addWidget(QLabel("Available Seat:"), 1, 0)
        booking_layout.addWidget(self._seat_combo, 1, 1)
        self._layout.addWidget(booking_group)

        # 5. Final Price and Confirmation
        self._price_label = QLabel("<h2>Final Price: ₹0.00</h2>")
        self._layout.addWidget(self._price_label)

        self._book_button = QPushButton("Confirm Booking")
        self._book_button.clicked.connect(self.confirm_booking)
        self._layout.addWidget(self._book_button)

        # Initial state setup
        self.reset_flight_selection()

    def reset_flight_selection(self):
        """Resets all flight, class, and seat related widgets."""
        self._flight_list.clear()
        self._flight_list.addItem("— Select Flight —")
        self._flight_details_label.setText("Select a route to view flights.")
        self._selected_flight = None
        
        if self._class_combo.currentIndex() != 0:
            self._class_combo.setCurrentIndex(0)
        self._seat_combo.clear()
        self._price_label.setText("<h2>Final Price: ₹0.00</h2>")
        self._book_button.setEnabled(False)


    def filter_flights(self):
        """Populates the flight combo box based on selected route."""
        self.reset_flight_selection()
        
        origin = self._origin_combo.currentText()
        destination = self._destination_combo.currentText()

        # Check if both Origin and Destination are selected (not the placeholder index 0)
        if self._origin_combo.currentIndex() == 0 or self._destination_combo.currentIndex() == 0:
            return

        available_flights = [
            f for f in self._booking_system._flights
            if f.get_origin() == origin and f.get_destination() == destination
        ]

        if not available_flights:
            self._flight_list.addItem("No flights available for this route")
        else:
            for flight in available_flights:
                flight_type = "Red-Eye" if hasattr(flight, 'DISCOUNT_RATE') else "Normal"
                flight_text = f"{flight.get_flight_number()} ({flight_type}) - ₹{flight.calculate_fare():.2f}"
                # Store the actual Flight object as user data
                self._flight_list.addItem(flight_text, flight)
            self._flight_list.setCurrentIndex(1) # Select the first actual flight


    def show_flight_details(self):
        """Displays selected flight details and enables class selection."""
        # Index 0 is the placeholder "— Select Flight —"
        if self._flight_list.currentIndex() == 0:
            self._selected_flight = None
            self._flight_details_label.setText("Select a flight to proceed.")
            self._class_combo.setCurrentIndex(0)
            self._seat_combo.clear()
            self._book_button.setEnabled(False)
            self._price_label.setText("<h2>Final Price: ₹0.00</h2>")
            return

        self._selected_flight = self._flight_list.currentData()
        
        if self._selected_flight:
            flight_type = "Red-Eye (10% off)" if hasattr(self._selected_flight, 'DISCOUNT_RATE') else "Normal"
            details = (
                f"Flight: **{self._selected_flight.get_flight_number()}** | "
                f"Type: {flight_type} | "
                f"Base Fare: **₹{self._selected_flight.calculate_fare():.2f}**"
            )
            self._flight_details_label.setText(details)
            # Reset class/seat selection but keep the button disabled until seat is chosen
            self._class_combo.setCurrentIndex(0)
            self._seat_combo.clear()
            self._book_button.setEnabled(False)
            self._price_label.setText("<h2>Final Price: ₹0.00</h2>")


    def populate_seats(self):
        """Populates the seat combo box based on selected class and flight."""
        self._seat_combo.clear()
        self._price_label.setText("<h2>Final Price: ₹0.00</h2>")
        self._book_button.setEnabled(False)

        # Index 0 is the placeholder "— Select Class —"
        if not self._selected_flight or self._class_combo.currentIndex() == 0:
            return

        # Get category index: 1, 2, or 3
        category_index = str(self._class_combo.currentIndex())
        CategoryClass = self.flight_category_map[category_index]
        category = CategoryClass()
        
        prefix = category.get_category_name()[0]
        available_seats = []
        for i in range(category.get_seat_range_start(), category.get_seat_range_end() + 1):
            seat = f"{prefix}{i}"
            if self._selected_flight.is_seat_available(seat):
                available_seats.append(seat)

        if not available_seats:
            QMessageBox.warning(self, "Seats Unavailable", f"❌ No seats available in **{category.get_category_name()}**!")
            return
        
        self._seat_combo.addItems(available_seats)
        self._seat_combo.setCurrentIndex(0)
        self.calculate_fare()
        self._book_button.setEnabled(True)


    def calculate_fare(self):
        """Calculates and displays the final price."""
        self._book_button.setEnabled(False)
        if not self._selected_flight or self._class_combo.currentIndex() == 0 or self._seat_combo.currentText() == "":
            self._price_label.setText("<h2>Final Price: ₹0.00</h2>")
            return

        category_index = str(self._class_combo.currentIndex())
        CategoryClass = self.flight_category_map[category_index]
        category = CategoryClass()
        
        final_price = self._selected_flight.calculate_fare() * category.get_price_multiplier()
        self._price_label.setText(f"<h2>Final Price: ₹{final_price:.2f}</h2>")
        self._book_button.setEnabled(True)


    def confirm_booking(self):
        """Final confirmation and calling the backend booking function."""
        passenger_name = self._name_input.text().strip()
        selected_seat = self._seat_combo.currentText()
        
        if not passenger_name:
            QMessageBox.warning(self, "Input Error", "Please enter the **Passenger Name**.")
            return

        if not selected_seat:
            QMessageBox.warning(self, "Input Error", "Please select a **seat**.")
            return

        if not self._selected_flight:
            QMessageBox.critical(self, "Selection Error", "No flight selected. Please choose a flight first.")
            return

        category_type = str(self._class_combo.currentIndex()) # '1', '2', or '3'
        class_name = self.flight_category_map[category_type]().get_category_name()
        
        # Confirmation Dialog
        flight_num = self._selected_flight.get_flight_number()
        price_text = self._price_label.text().replace('<h2>','').replace('</h2>','')
        reply = QMessageBox.question(
            self, 'Confirm Booking', 
            (f"Confirm booking for **{passenger_name}** on flight **{flight_num}** "
             f"in **{class_name}** (Seat: {selected_seat}) for **{price_text}**?"), 
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Create booking using the backend system
            booking = self._booking_system.create_booking(
                passenger_name, 
                flight_num,
                category_type, 
                selected_seat
            )

            if booking:
                QMessageBox.information(self, "Booking Confirmed", f"Booking Successful! Your ID is **{booking.get_booking_id()}**.")
                self.accept()
            else:
                # This should ideally not happen if checks pass, but for safety:
                QMessageBox.critical(self, "Booking Failed", "An error occurred during booking.")
        # If reply is No, the dialog remains open