import os
import mysql.connector

# DATABASE CONNECTION
conn = mysql.connector.connect(
    host=os.getenv("SPORTS_DB_HOST", "localhost"),
    user=os.getenv("SPORTS_DB_USER", "root"),
    password=os.getenv("SPORTS_DB_PASSWORD"),
    database=os.getenv("SPORTS_DB_NAME", "sports_ecommerce")
)
cursor = conn.cursor()


# PRODUCT FUNCTIONS
def insert_product():
    try:
        name = input("Enter product name: ")
        category = input("Enter product category: ")
        price = float(input("Enter product price (without ₹): "))
        stock = int(input("Enter stock quantity: "))
        description = input("Enter product description: ")

        query = """
        INSERT INTO products (name, category, price, stock, description)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, category, price, stock, description))
        conn.commit()
        print("✅ Product added successfully!")
    except Exception as e:
        print("❌ Error inserting product:", e)


def view_products():
    try:
        cursor.execute("SELECT product_id, name, category, price, stock, description FROM products")
        results = cursor.fetchall()
        if results:
            print("\n------ 🏋️‍♂️ Product List ------")
            for row in results:
                print(f"ID: {row[0]} | Name: {row[1]} | Category: {row[2]} | Price: ₹{row[3]} | Stock: {row[4]} | Desc: {row[5]}")
            print("--------------------------\n")
        else:
            print("No products found.")
    except Exception as e:
        print("❌ Error displaying products:", e)


def update_product():
    try:
        product_id = int(input("Enter Product ID to update: "))
        print("\nChoose the field to update:")
        print("1. Name")
        print("2. Category")
        print("3. Price")
        print("4. Stock")
        print("5. Description")

        choice = int(input("Enter your choice (1-5): "))
        fields = ["name", "category", "price", "stock", "description"]

        if 1 <= choice <= 5:
            new_value = input("Enter new value: ")
            if fields[choice - 1] == "price":
                new_value = float(new_value)
            elif fields[choice - 1] == "stock":
                new_value = int(new_value)

            query = f"UPDATE products SET {fields[choice - 1]} = %s WHERE product_id = %s"
            cursor.execute(query, (new_value, product_id))
            conn.commit()

            if cursor.rowcount > 0:
                print("✅ Product updated successfully!")
            else:
                print("❌ No product found with that ID.")
        else:
            print("❌ Invalid choice.")
    except Exception as e:
        print("❌ Error updating product:", e)


def delete_product():
    try:
        product_id = int(input("Enter Product ID to delete: "))
        cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
        conn.commit()

        if cursor.rowcount > 0:
            print("🗑️ Product deleted successfully!")
        else:
            print("❌ No product found with that ID.")
    except Exception as e:
        print("❌ Error deleting product:", e)


def search_product():
    try:
        keyword = input("Enter product name or category to search: ")
        query = "SELECT * FROM products WHERE name LIKE %s OR category LIKE %s"
        cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
        results = cursor.fetchall()

        if results:
            print("\n🔍 Search Results:")
            for row in results:
                print(f"ID: {row[0]} | Name: {row[1]} | Category: {row[2]} | Price: ₹{row[3]} | Stock: {row[4]} | Desc: {row[5]}")
        else:
            print("❌ No matching products found.")
    except Exception as e:
        print("❌ Error searching for product:", e)


# USER FUNCTIONS
def view_users():
    try:
        cursor.execute("SELECT user_id, name, email, phone, created_at FROM users")
        results = cursor.fetchall()
        if results:
            print("\n👤 USERS LIST:")
            for row in results:
                print(f"ID: {row[0]} | Name: {row[1]} | Email: {row[2]} | Phone: {row[3]} | Joined: {row[4]}")
        else:
            print("No users found.")
    except Exception as e:
        print("❌ Error fetching users:", e)


#  ORDER FUNCTIONS 
def view_orders():
    try:
        query = """
        SELECT o.order_id, u.name AS user_name, o.order_date, o.total_amount, o.status
        FROM orders o
        LEFT JOIN users u ON o.user_id = u.user_id
        ORDER BY o.order_date DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        if results:
            print("\n📦 ORDERS LIST:")
            for row in results:
                print(f"Order ID: {row[0]} | Customer: {row[1]} | Date: {row[2]} | Amount: ₹{row[3]} | Status: {row[4]}")
        else:
            print("No orders found.")
    except Exception as e:
        print("❌ Error fetching orders:", e)


def view_order_items():
    try:
        order_id = int(input("Enter Order ID to view items: "))
        query = """
        SELECT p.name, oi.quantity, oi.unit_price
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        WHERE oi.order_id = %s
        """
        cursor.execute(query, (order_id,))
        results = cursor.fetchall()
        if results:
            print(f"\n🛒 Items in Order {order_id}:")
            for row in results:
                print(f"- {row[0]} (x{row[1]}) - ₹{row[2]}")
        else:
            print("No items found for this order.")
    except Exception as e:
        print("❌ Error fetching order items:", e)


# MAIN MENU
def main():
    while True:
        print("\n===== 🏀 SPORTS E-COMMERCE BACKEND =====")
        print("1. Insert Product")
        print("2. View Products")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Search Product")
        print("6. View Users")
        print("7. View Orders")
        print("8. View Order Items")
        print("9. Exit")

        choice = input("Enter your choice (1-9): ")

        if choice == '1':
            insert_product()
        elif choice == '2':
            view_products()
        elif choice == '3':
            update_product()
        elif choice == '4':
            delete_product()
        elif choice == '5':
            search_product()
        elif choice == '6':
            view_users()
        elif choice == '7':
            view_orders()
        elif choice == '8':
            view_order_items()
        elif choice == '9':
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")


# RUN PROGRAM
if __name__ == "__main__":
    main()

cursor.close()
conn.close()
