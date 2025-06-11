import sqlite3

def get_connection():
    """Get database connection"""
    return sqlite3.connect('ecommerce.db')

def add_product(name, description, price, stock_quantity):
    """Add a new product to the database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO Products (product_name, description, price, stock_quantity)
        VALUES (?, ?, ?, ?)
    ''', (name, description, price, stock_quantity))
    
    product_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {"success": True, "product_id": product_id, "message": f"Product '{name}' added successfully"}

def remove_product(product_id):
    """Remove a product from the database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if product exists
    cursor.execute('SELECT product_name FROM Products WHERE product_id = ?', (product_id,))
    product = cursor.fetchone()
    
    if not product:
        conn.close()
        return {"success": False, "message": "Product not found"}
    
    # Remove product
    cursor.execute('DELETE FROM Products WHERE product_id = ?', (product_id,))
    conn.commit()
    conn.close()
    
    return {"success": True, "message": f"Product '{product[0]}' removed successfully"}

def show_products():
    """Show all products in the database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT product_id, product_name, description, price, stock_quantity
        FROM Products
        ORDER BY product_name
    ''')
    
    products = cursor.fetchall()
    conn.close()
    
    if not products:
        return {"success": True, "products": [], "message": "No products found"}
    
    product_list = []
    for product in products:
        product_list.append({
            "product_id": product[0],
            "name": product[1],
            "description": product[2],
            "price": product[3],
            "stock": product[4]
        })
    
    return {"success": True, "products": product_list, "count": len(product_list)}