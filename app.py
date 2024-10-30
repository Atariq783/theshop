import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry  # Ensure tkcalendar is installed
import json
import hashlib
import os

# Function to load JSON data
def load_data(file_name):
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Function to save JSON data
def save_data(file_name, data):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Login function
def login():
    email = email_entry.get().strip()
    password = password_entry.get().strip()
    users = load_data('users.json')
    hashed_password = hash_password(password)

    for user in users.values():
        if user['Email'] == email and user['Password'] == hashed_password:
            if user['Role'] == 'Admin':
                messagebox.showinfo("Success", "Welcome, Admin!")
                show_frame(dashboard_frame)
                view_bookings()
                return
            else:
                messagebox.showwarning("Access Denied", "Admin access required.")
                return

    messagebox.showerror("Login Failed", "Invalid credentials.")

# Function to add a booking
def add_booking():
    user_id = user_id_entry.get()
    service_type = service_entry.get()
    booking_date = date_picker.get_date().strftime('%Y-%m-%d')

    if not user_id or not service_type:
        messagebox.showerror("Error", "All fields are required!")
        return

    bookings = load_data('bookings.json')
    booking_id = str(len(bookings) + 1)

    new_booking = {
        "UserID": user_id,
        "ServiceType": service_type,
        "BookingDate": booking_date,
        "BookingStatus": "Upcoming"
    }

    bookings[booking_id] = new_booking
    save_data('bookings.json', bookings)
    messagebox.showinfo("Success", "Booking added successfully!")
    view_bookings()

# Function to display bookings
def view_bookings():
    bookings = load_data('bookings.json')
    bookings_list.delete(0, tk.END)
    for booking_id, details in bookings.items():
        booking_info = f"{booking_id}: {details['ServiceType']} on {details['BookingDate']} - {details['BookingStatus']}"
        bookings_list.insert(tk.END, booking_info)

# Function to switch frames
def show_frame(frame):
    frame.tkraise()

# Logout function
def logout():
    email_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    show_frame(login_frame)

# Main application window
root = tk.Tk()
root.title("THE SHOP - Management System")
root.geometry("800x600")

# Define frames
login_frame = tk.Frame(root)
dashboard_frame = tk.Frame(root)
booking_frame = tk.Frame(root)

for frame in (login_frame, dashboard_frame, booking_frame):
    frame.grid(row=0, column=0, sticky='nsew')

# --- Login Frame ---
tk.Label(login_frame, text="Login", font=("Arial", 24)).pack(pady=20)

tk.Label(login_frame, text="Email:", font=("Arial", 14)).pack(pady=5)
email_entry = tk.Entry(login_frame, width=30)
email_entry.pack(pady=5)

tk.Label(login_frame, text="Password:", font=("Arial", 14)).pack(pady=5)
password_entry = tk.Entry(login_frame, show="*", width=30)
password_entry.pack(pady=5)

tk.Button(login_frame, text="Login", command=login, width=20, font=("Arial", 14)).pack(pady=20)

# --- Dashboard Frame ---
tk.Label(dashboard_frame, text="Dashboard", font=("Arial", 24)).pack(pady=20)

bookings_list = tk.Listbox(dashboard_frame, width=80, height=15)
bookings_list.pack(pady=10)

tk.Button(dashboard_frame, text="Add Booking", command=lambda: show_frame(booking_frame), width=20, font=("Arial", 14)).pack(pady=10)
tk.Button(dashboard_frame, text="Logout", command=logout, width=20, font=("Arial", 14)).pack(pady=10)

# --- Booking Frame ---
tk.Label(booking_frame, text="Add Booking", font=("Arial", 24)).pack(pady=20)

tk.Label(booking_frame, text="User ID:", font=("Arial", 14)).pack(pady=5)
user_id_entry = tk.Entry(booking_frame, width=30)
user_id_entry.pack(pady=5)

tk.Label(booking_frame, text="Service Type:", font=("Arial", 14)).pack(pady=5)
service_entry = tk.Entry(booking_frame, width=30)
service_entry.pack(pady=5)

tk.Label(booking_frame, text="Booking Date:", font=("Arial", 14)).pack(pady=5)
date_picker = DateEntry(booking_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
date_picker.pack(pady=5)

tk.Button(booking_frame, text="Submit", command=add_booking, width=20, font=("Arial", 14)).pack(pady=20)
tk.Button(booking_frame, text="Back to Dashboard", command=lambda: show_frame(dashboard_frame), width=20, font=("Arial", 14)).pack(pady=10)

# Start with the login frame
show_frame(login_frame)

# Run the application
root.mainloop()
