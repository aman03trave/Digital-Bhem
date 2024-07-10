import tkinter as tk
from tkinter import messagebox
import sqlite3

# Function to create database connection
def connect_db():
    return sqlite3.connect('bmi_calculator.db')

# Function to create a user
def create_user(username, password, name, age, height, weight):
    conn = connect_db()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, name, age, height, weight) VALUES (?, ?, ?, ?, ?, ?)",
                  (username, password, name, age, height, weight))
        conn.commit()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists")
    conn.close()

# Function to verify user credentials
def verify_user(username, password):
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user

# Main Application Class
class BMICalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")
        self.root.geometry("400x400")

        self.show_login_page()

    def show_login_page(self):
        self.clear_screen()

        tk.Label(self.root, text="Login", font=("Helvetica", 16)).pack(pady=20)

        tk.Label(self.root, text="Username").pack()
        self.login_username_entry = tk.Entry(self.root)
        self.login_username_entry.pack()

        tk.Label(self.root, text="Password").pack()
        self.login_password_entry = tk.Entry(self.root, show="*")
        self.login_password_entry.pack()

        tk.Button(self.root, text="Login", command=self.login).pack(pady=20)
        tk.Button(self.root, text="Sign Up", command=self.show_signup_page).pack()

    def show_signup_page(self):
        self.clear_screen()

        tk.Label(self.root, text="Sign Up", font=("Helvetica", 16)).pack(pady=20)

        tk.Label(self.root, text="Username").pack()
        self.signup_username_entry = tk.Entry(self.root)
        self.signup_username_entry.pack()

        tk.Label(self.root, text="Password").pack()
        self.signup_password_entry = tk.Entry(self.root, show="*")
        self.signup_password_entry.pack()

        tk.Label(self.root, text="Name").pack()
        self.signup_name_entry = tk.Entry(self.root)
        self.signup_name_entry.pack()

        tk.Label(self.root, text="Age").pack()
        self.signup_age_entry = tk.Entry(self.root)
        self.signup_age_entry.pack()

        tk.Label(self.root, text="Height (cm)").pack()
        self.signup_height_entry = tk.Entry(self.root)
        self.signup_height_entry.pack()

        tk.Label(self.root, text="Weight (kg)").pack()
        self.signup_weight_entry = tk.Entry(self.root)
        self.signup_weight_entry.pack()

        tk.Button(self.root, text="Sign Up", command=self.signup).pack(pady=20)
        tk.Button(self.root, text="Back to Login", command=self.show_login_page).pack()

    def show_dashboard(self, user):
        self.clear_screen()

        self.user = user

        tk.Label(self.root, text=f"Welcome, {self.user[3]}", font=("Helvetica", 16)).pack(pady=20)

        tk.Label(self.root, text=f"Age: {self.user[4]}").pack()
        tk.Label(self.root, text=f"Height: {self.user[5]} cm").pack()
        tk.Label(self.root, text=f"Weight: {self.user[6]} kg").pack()

        bmi = self.calculate_bmi()
        classification = self.classify_bmi(bmi)

        tk.Label(self.root, text=f"BMI: {bmi:.2f}").pack(pady=10)
        tk.Label(self.root, text=f"Classification: {classification}").pack(pady=10)

        tk.Button(self.root, text="Update Details", command=self.show_update_page).pack(pady=20)
        tk.Button(self.root, text="Logout", command=self.show_login_page).pack()

    def show_update_page(self):
        self.clear_screen()

        tk.Label(self.root, text="Update Details", font=("Helvetica", 16)).pack(pady=20)

        tk.Label(self.root, text="Age").pack()
        self.update_age_entry = tk.Entry(self.root)
        self.update_age_entry.insert(0, self.user[4])
        self.update_age_entry.pack()

        tk.Label(self.root, text="Height (cm)").pack()
        self.update_height_entry = tk.Entry(self.root)
        self.update_height_entry.insert(0, self.user[5])
        self.update_height_entry.pack()

        tk.Label(self.root, text="Weight (kg)").pack()
        self.update_weight_entry = tk.Entry(self.root)
        self.update_weight_entry.insert(0, self.user[6])
        self.update_weight_entry.pack()

        tk.Button(self.root, text="Update", command=self.update_user_details).pack(pady=20)
        tk.Button(self.root, text="Back to Dashboard", command=lambda: self.show_dashboard(self.user)).pack()

    def login(self):
        username = self.login_username_entry.get()
        password = self.login_password_entry.get()

        user = verify_user(username, password)
        if user:
            self.show_dashboard(user)
        else:
            messagebox.showerror("Error", "Invalid credentials or user does not exist")

    def signup(self):
        username = self.signup_username_entry.get()
        password = self.signup_password_entry.get()
        name = self.signup_name_entry.get()
        age = self.signup_age_entry.get()
        height = self.signup_height_entry.get()
        weight = self.signup_weight_entry.get()

        if username and password and name and age and height and weight:
            create_user(username, password, name, age, height, weight)
            messagebox.showinfo("Success", "Account created successfully")
            self.show_login_page()
        else:
            messagebox.showerror("Error", "All fields are required")

    def update_user_details(self):
        age = self.update_age_entry.get()
        height = self.update_height_entry.get()
        weight = self.update_weight_entry.get()

        conn = connect_db()
        c = conn.cursor()
        c.execute("UPDATE users SET age=?, height=?, weight=? WHERE id=?",
                  (age, height, weight, self.user[0]))
        conn.commit()
        conn.close()

        self.user = (self.user[0], self.user[1], self.user[2], self.user[3], int(age), float(height), float(weight))
        messagebox.showinfo("Success", "Details updated successfully")
        self.show_dashboard(self.user)

    def calculate_bmi(self):
        height_m = self.user[5] / 100  # Convert height from cm to meters
        weight_kg = self.user[6]
        bmi = weight_kg / (height_m ** 2)
        return bmi

    def classify_bmi(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Create the main window
root = tk.Tk()
app = BMICalculatorApp(root)
root.mainloop()
