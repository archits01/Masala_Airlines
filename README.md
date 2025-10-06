# MASALA AIRLINES Flight Booking System

A modular Python application for airline ticket booking with a console-based interface.

## Project Structure

The application has been refactored into separate modules for better organization:

### 📁 Module Overview

- **`main.py`** - Entry point of the application
  - Initializes flight data (20 hardcoded flights)
  - Starts the console UI

- **`flights.py`** - Flight-related classes
  - `Flight` (abstract base class)
  - `NormalFlight` (standard flights)
  - `RedEyeFlight` (discounted night flights)

- **`categories.py`** - Booking category classes
  - `BookingCategory` (abstract base class)
  - `FirstClass` (F1-F10, 3x multiplier)
  - `Business` (B11-B30, 2x multiplier)
  - `Economy` (E31-E60, 1x multiplier)

- **`booking.py`** - Booking management
  - `Booking` (individual booking records)
  - `BookingSystem` (manages flights and bookings)

- **`ui.py`** - User interface
  - `ConsoleUI` (menu system and user interactions)

## 🚀 How to Run

```bash
python3 main.py
```

## ✨ Features

- View available flights
- Search flights by route
- Book tickets with seat selection
- Multiple booking categories (First, Business, Economy)
- View and cancel bookings
- Interactive console interface

## 🎯 Flight Types

- **Normal Flights**: Standard pricing
- **Red-Eye Flights**: 10% discount on base fare

## 💺 Seat Categories

- **First Class (F1-F10)**: Premium seats, gourmet meals, priority boarding
- **Business (B11-B30)**: Comfortable seats, meals included, priority check-in
- **Economy (E31-E60)**: Standard seats, snacks available

All functionality remains identical to the original single-file version, just better organized!
