import os
import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
import time
import threading

# DATABASE CONNECTION
def connect_db():
    return mysql.connector.connect(
        host=os.getenv("SPORTS_DB_HOST", "localhost"),
        user=os.getenv("SPORTS_DB_USER", "root"),
        password=os.getenv("SPORTS_DB_PASSWORD"),
        database=os.getenv("SPORTS_DB_NAME", "sports_ecommerce")
    )

#APP SETUP
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Sports E-Commerce 🏀")
app.geometry("1100x700")
app.resizable(False, False)

# HELPER FUNCTIONS
def clear_frame():
    for widget in main_frame.winfo_children():
        widget.destroy()

def back_to_home():
    clear_frame()
    create_dashboard()

def display_table(parent, headers, rows):
    frame = ctk.CTkScrollableFrame(parent, fg_color="white")
    frame.pack(pady=10, padx=20, fill="both", expand=True)

    for i, header in enumerate(headers):
        lbl = ctk.CTkLabel(frame, text=header, font=("Helvetica", 15, "bold"), text_color="#005f73")
        lbl.grid(row=0, column=i, padx=15, pady=10)

    for r, row in enumerate(rows, start=1):
        for c, val in enumerate(row):
            lbl = ctk.CTkLabel(frame, text=val, font=("Helvetica", 13))
            lbl.grid(row=r, column=c, padx=15, pady=6)

#LOGIN PAGE
def login_page():
    clear_frame()
    ctk.CTkLabel(main_frame, text="🏀 SPORTS E-COMMERCE LOGIN", font=("Helvetica", 26, "bold"), text_color="#005f73").pack(pady=30)

    frame = ctk.CTkFrame(main_frame, width=400, height=250, corner_radius=15)
    frame.pack(pady=20)

    username_entry = ctk.CTkEntry(frame, width=250, placeholder_text="Username")
    password_entry = ctk.CTkEntry(frame, width=250, placeholder_text="Password", show="*")
    username_entry.pack(pady=15)
    password_entry.pack(pady=10)

    def login_action():
        username = username_entry.get()
        password = password_entry.get()
        expected_username = os.getenv("SPORTS_ADMIN_USERNAME")
        expected_password = os.getenv("SPORTS_ADMIN_PASSWORD")
        if not expected_username or not expected_password:
            messagebox.showerror(
                "Configuration Required",
                "Set SPORTS_ADMIN_USERNAME and SPORTS_ADMIN_PASSWORD environment variables before logging in."
            )
            return
        if username == expected_username and password == expected_password:
            messagebox.showinfo("Login Successful", "Welcome, Admin!")
            clear_frame()
            create_dashboard()
        else:
            messagebox.showerror("Invalid", "Incorrect username or password.")

    ctk.CTkButton(frame, text="Login", fg_color="#0a9396", command=login_action).pack(pady=20)

#SPLASH SCREEN
def splash_screen():
    splash = ctk.CTkToplevel(app)
    splash.geometry("500x300+350+200")
    splash.title("Welcome 🏆")
    splash.configure(fg_color="white")
    splash.resizable(False, False)

    ctk.CTkLabel(splash, text="SPORTS E-COMMERCE", font=("Helvetica", 28, "bold"), text_color="#0a9396").pack(pady=50)
    ctk.CTkLabel(splash, text="Loading your dashboard...", font=("Helvetica", 16)).pack(pady=20)

    progress = ctk.CTkProgressBar(splash, width=350, progress_color="#0a9396")
    progress.set(0)
    progress.pack(pady=20)

    def load():
        for i in range(101):
            time.sleep(0.03)
            progress.set(i / 100)
        splash.destroy()
        login_page()

    threading.Thread(target=load).start()

# PRODUCT FUNCTIONS
def add_product_page():
    clear_frame()
    ctk.CTkLabel(main_frame, text="➕ Add Product", font=("Helvetica", 22, "bold")).pack(pady=15)
    frame = ctk.CTkFrame(main_frame)
    frame.pack(pady=20)

    name = ctk.CTkEntry(frame, width=200, placeholder_text="Product Name")
    category = ctk.CTkEntry(frame, width=200, placeholder_text="Category")
    price = ctk.CTkEntry(frame, width=200, placeholder_text="Price (₹)")
    stock = ctk.CTkEntry(frame, width=200, placeholder_text="Stock Quantity")
    description = ctk.CTkEntry(frame, width=300, placeholder_text="Description")

    entries = [name, category, price, stock, description]
    for i, e in enumerate(entries):
        e.grid(row=i//2, column=i%2, padx=10, pady=10)

    def add_product():
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO products (name, category, price, stock, description)
                VALUES (%s,%s,%s,%s,%s)
            """, (name.get(), category.get(), float(price.get()), int(stock.get()), description.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "✅ Product added successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ctk.CTkButton(frame, text="Add Product", fg_color="#0a9396", command=add_product).grid(row=3, column=0, columnspan=2, pady=20)
    ctk.CTkButton(main_frame, text="⬅ Back", fg_color="#0a9396", command=back_to_home).pack(side="bottom", pady=15)

def view_products_page():
    clear_frame()
    ctk.CTkLabel(main_frame, text="📦 View Products", font=("Helvetica", 22, "bold")).pack(pady=15)
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT product_id, name, category, price, stock FROM products")
        rows = cur.fetchall()
        headers = ["ID", "Name", "Category", "Price (₹)", "Stock"]
        display_table(main_frame, headers, rows)
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))
    ctk.CTkButton(main_frame, text="⬅ Back", fg_color="#0a9396", command=back_to_home).pack(pady=20)

def search_product_page():
    clear_frame()
    ctk.CTkLabel(main_frame, text="🔍 Search Product", font=("Helvetica", 22, "bold")).pack(pady=15)
    frame = ctk.CTkFrame(main_frame)
    frame.pack(pady=10)

    entry = ctk.CTkEntry(frame, width=300, placeholder_text="Enter product name or category...")
    entry.grid(row=0, column=0, padx=10)

    result_frame = ctk.CTkFrame(main_frame)
    result_frame.pack(fill="both", expand=True, pady=10)

    def search_action():
        for w in result_frame.winfo_children():
            w.destroy()
        term = entry.get().strip()
        if not term:
            messagebox.showwarning("Empty", "Please enter a search term.")
            return
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM products WHERE name LIKE %s OR category LIKE %s", (f"%{term}%", f"%{term}%"))
        rows = cur.fetchall()
        conn.close()
        headers = ["ID", "Name", "Category", "Price", "Stock", "Description"]
        display_table(result_frame, headers, rows)

    ctk.CTkButton(frame, text="Search", fg_color="#0a9396", command=search_action).grid(row=0, column=1, padx=10)
    ctk.CTkButton(main_frame, text="⬅ Back", fg_color="#0a9396", command=back_to_home).pack(side="bottom", pady=15)

#USERS AND ORDERS
def view_users_page():
    clear_frame()
    ctk.CTkLabel(main_frame, text="👥 View Users", font=("Helvetica", 22, "bold")).pack(pady=15)
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT user_id, name, email, phone, created_at FROM users")
        rows = cur.fetchall()
        headers = ["User ID", "Name", "Email", "Phone", "Created At"]
        display_table(main_frame, headers, rows)
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))
    ctk.CTkButton(main_frame, text="⬅ Back", fg_color="#0a9396", command=back_to_home).pack(pady=15)

def view_orders_page():
    clear_frame()
    ctk.CTkLabel(main_frame, text="🧾 Orders", font=("Helvetica", 22, "bold")).pack(pady=15)
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT o.order_id, u.name AS user, o.total_amount, o.status, o.order_date
            FROM orders o
            JOIN users u ON o.user_id = u.user_id
        """)
        rows = cur.fetchall()
        headers = ["Order ID", "User", "Total (₹)", "Status", "Date"]
        display_table(main_frame, headers, rows)
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))
    ctk.CTkButton(main_frame, text="⬅ Back", fg_color="#0a9396", command=back_to_home).pack(pady=15)

# DASHBOARD
def create_dashboard():
    ctk.CTkLabel(main_frame, text="🏀 SPORTS E-COMMERCE DASHBOARD", font=("Helvetica", 26, "bold")).pack(pady=25)
    grid = ctk.CTkFrame(main_frame, fg_color="#edf6f9", corner_radius=15)
    grid.pack(pady=20)
    grid.grid_columnconfigure((0, 1, 2), weight=1)
    grid.grid_rowconfigure((0, 1), weight=1)

    buttons = [
        ("Add Product", "Add new sports product.", add_product_page),
        ("View Products", "See all available products.", view_products_page),
        ("Search Product", "Search products by name or category.", search_product_page),
        ("View Users", "View registered users.", view_users_page),
        ("View Orders", "Check customer orders.", view_orders_page)
    ]

    r, c = 0, 0
    for title, desc, cmd in buttons:
        frame = ctk.CTkFrame(grid, corner_radius=15, fg_color="white", width=280, height=160)
        frame.pack_propagate(False)
        frame.grid(row=r, column=c, padx=20, pady=20)
        ctk.CTkLabel(frame, text=title, font=("Helvetica", 18, "bold"), text_color="#005f73").pack(pady=10)
        ctk.CTkLabel(frame, text=desc, font=("Helvetica", 13), wraplength=220).pack(pady=5)
        ctk.CTkButton(frame, text="Open", fg_color="#0a9396", command=cmd).pack(pady=10)
        c += 1
        if c == 3:
            c = 0
            r += 1

# MAIN FRAME
main_frame = ctk.CTkFrame(app, fg_color="white")
main_frame.pack(fill="both", expand=True)

# Start with splash screen
splash_screen()
app.mainloop()
