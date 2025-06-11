import sqlite3

def get_connection():
    """Get database connection"""
    return sqlite3.connect('ecommerce.db')

def add_to_cart(customer_id, product_id, quantity):
    """Add products to cart"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if product exists and has enough stock
    cursor.execute('SELECT product_name, stock_quantity FROM Products WHERE product_id = ?', (product_id,))
    product = cursor.fetchone()
    
    if not product:
        conn.close()
        return {"success": False, "message": "Product not found"}
    
    if product[1] < quantity:
        conn.close()
        return {"success": False, "message": f"Insufficient stock. Only {product[1]} available"}
    
    # Check if item already in cart
    cursor.execute('SELECT cart_id, quantity FROM Carts WHERE customer_id = ? AND product_id = ?', 
                   (customer_id, product_id))
    existing = cursor.fetchone()
    
    if existing:
        # Update quantity
        new_quantity = existing[1] + quantity
        cursor.execute('UPDATE Carts SET quantity = ? WHERE cart_id = ?', (new_quantity, existing[0]))
    else:
        # Add new item
        cursor.execute('INSERT INTO Carts (customer_id, product_id, quantity) VALUES (?, ?, ?)',
                       (customer_id, product_id, quantity))
    
    conn.commit()
    conn.close()
    
    return {"success": True, "message": f"Added {quantity} {product[0]}(s) to cart"}

def remove_from_cart(customer_id, product_id, quantity=None):
    """Remove products from cart"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Find cart item
    cursor.execute('SELECT cart_id, quantity FROM Carts WHERE customer_id = ? AND product_id = ?', 
                   (customer_id, product_id))
    cart_item = cursor.fetchone()
    
    if not cart_item:
        conn.close()
        return {"success": False, "message": "Item not found in cart"}
    
    if quantity is None or quantity >= cart_item[1]:
        # Remove entire item
        cursor.execute('DELETE FROM Carts WHERE cart_id = ?', (cart_item[0],))
        message = "Item removed from cart"
    else:
        # Reduce quantity
        new_quantity = cart_item[1] - quantity
        cursor.execute('UPDATE Carts SET quantity = ? WHERE cart_id = ?', (new_quantity, cart_item[0]))
        message = f"Removed {quantity} item(s) from cart"
    
    conn.commit()
    conn.close()
    
    return {"success": True, "message": message}

def drop_cart(customer_id):
    """Drop entire cart for a customer"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if cart has items
    cursor.execute('SELECT COUNT(*) FROM Carts WHERE customer_id = ?', (customer_id,))
    count = cursor.fetchone()[0]
    
    if count == 0:
        conn.close()
        return {"success": False, "message": "Cart is already empty"}
    
    # Drop cart
    cursor.execute('DELETE FROM Carts WHERE customer_id = ?', (customer_id,))
    conn.commit()
    conn.close()
    
    return {"success": True, "message": f"Cart cleared. {count} item(s) removed"}

def show_cart(customer_id):
    """Show cart contents for a customer"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT c.cart_id, p.product_name, p.price, c.quantity, (p.price * c.quantity) as total
        FROM Carts c
        JOIN Products p ON c.product_id = p.product_id
        WHERE c.customer_id = ?
        ORDER BY p.product_name
    ''', (customer_id,))
    
    items = cursor.fetchall()
    conn.close()
    
    if not items:
        return {"success": True, "cart": [], "total": 0, "message": "Cart is empty"}
    
    cart_items = []
    total_amount = 0
    
    for item in items:
        cart_items.append({
            "cart_id": item[0],
            "product_name": item[1],
            "price": item[2],
            "quantity": item[3],
            "total": item[4]
        })
        total_amount += item[4]
    
    return {"success": True, "cart": cart_items, "total": total_amount, "count": len(cart_items)}