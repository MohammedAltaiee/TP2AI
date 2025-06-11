import sqlite3
from datetime import datetime, date

def create_database():
    """Create and populate all tables for the eCommerce database"""
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    # Create Customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            address TEXT
        )
    ''')
    
    # Create Products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name VARCHAR(255) NOT NULL,
            description TEXT,
            price DECIMAL(10, 2) NOT NULL,
            stock_quantity INTEGER NOT NULL DEFAULT 0
        )
    ''')
    
    # Create Orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            order_date DATE NOT NULL,
            total_amount DECIMAL(10, 2) NOT NULL DEFAULT 0,
            status VARCHAR(50) NOT NULL DEFAULT 'pending',
            FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
        )
    ''')
    
    # Create Order_Items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Order_Items (
            order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (order_id) REFERENCES Orders(order_id),
            FOREIGN KEY (product_id) REFERENCES Products(product_id)
        )
    ''')
    
    # Create Carts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Carts (
            cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
            FOREIGN KEY (product_id) REFERENCES Products(product_id)
        )
    ''')
    
    # Insert sample data
    populate_sample_data(cursor)
    
    conn.commit()
    conn.close()
    print("Database created and populated successfully!")

def populate_sample_data(cursor):
    """Populate tables with sample data"""
    
    # Sample customers
    customers = [
        ('John', 'Doe', 'john.doe@email.com', '123 Main St'),
        ('Jane', 'Smith', 'jane.smith@email.com', '456 Oak Ave'),
        ('Bob', 'Johnson', 'bob.johnson@email.com', '789 Pine Rd')
    ]
    cursor.executemany('INSERT INTO Customers (first_name, last_name, email, address) VALUES (?, ?, ?, ?)', customers)
    
    # Sample products
    products = [
        ('Laptop', 'High-performance laptop', 999.99, 10),
        ('Mouse', 'Wireless optical mouse', 29.99, 50),
        ('Keyboard', 'Mechanical keyboard', 79.99, 25),
        ('Monitor', '24-inch LED monitor', 199.99, 15),
        ('Headphones', 'Noise-canceling headphones', 149.99, 30)
    ]
    cursor.executemany('INSERT INTO Products (product_name, description, price, stock_quantity) VALUES (?, ?, ?, ?)', products)
    
    # Sample orders
    orders = [
        (1, date.today().isoformat(), 1029.98, 'completed'),
        (2, date.today().isoformat(), 229.98, 'pending'),
        (3, date.today().isoformat(), 79.99, 'shipped')
    ]
    cursor.executemany('INSERT INTO Orders (customer_id, order_date, total_amount, status) VALUES (?, ?, ?, ?)', orders)
    
    # Sample order items
    order_items = [
        (1, 1, 1, 999.99),  # Order 1: Laptop
        (1, 2, 1, 29.99),   # Order 1: Mouse
        (2, 4, 1, 199.99),  # Order 2: Monitor
        (2, 2, 1, 29.99),   # Order 2: Mouse
        (3, 3, 1, 79.99)    # Order 3: Keyboard
    ]
    cursor.executemany('INSERT INTO Order_Items (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)', order_items)
    
    # Sample cart items
    cart_items = [
        (2, 5, 1),  # Jane has headphones in cart
        (3, 1, 1),  # Bob has laptop in cart
        (3, 3, 2)   # Bob has 2 keyboards in cart
    ]
    cursor.executemany('INSERT INTO Carts (customer_id, product_id, quantity) VALUES (?, ?, ?)', cart_items)

if __name__ == "__main__":
    create_database()