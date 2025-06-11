import sqlite3
from datetime import date

def get_connection():
    """Get database connection"""
    return sqlite3.connect('ecommerce.db')

def create_order(customer_id, items, status='pending'):
    """Create new order with items list: [(product_id, quantity), ...]"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Calculate total and validate items
        total_amount = 0
        order_items = []
        
        for product_id, quantity in items:
            cursor.execute('SELECT product_name, price, stock_quantity FROM Products WHERE product_id = ?', 
                          (product_id,))
            product = cursor.fetchone()
            
            if not product:
                return {"success": False, "message": f"Product ID {product_id} not found"}
            
            if product[2] < quantity:
                return {"success": False, "message": f"Insufficient stock for {product[0]}"}
            
            item_total = product[1] * quantity
            total_amount += item_total
            order_items.append((product_id, quantity, product[1]))
        
        # Create order
        cursor.execute('''
            INSERT INTO Orders (customer_id, order_date, total_amount, status)
            VALUES (?, ?, ?, ?)
        ''', (customer_id, date.today().isoformat(), total_amount, status))
        
        order_id = cursor.lastrowid
        
        # Add order items and update stock
        for product_id, quantity, unit_price in order_items:
            cursor.execute('''
                INSERT INTO Order_Items (order_id, product_id, quantity, unit_price)
                VALUES (?, ?, ?, ?)
            ''', (order_id, product_id, quantity, unit_price))
            
            cursor.execute('UPDATE Products SET stock_quantity = stock_quantity - ? WHERE product_id = ?',
                          (quantity, product_id))
        
        conn.commit()
        conn.close()
        
        return {"success": True, "order_id": order_id, "total": total_amount, 
                "message": f"Order created successfully with ID {order_id}"}
        
    except Exception as e:
        conn.rollback()
        conn.close()
        return {"success": False, "message": f"Error creating order: {str(e)}"}

def delete_order(order_id):
    """Delete an order and restore stock"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Get order items to restore stock
        cursor.execute('SELECT product_id, quantity FROM Order_Items WHERE order_id = ?', (order_id,))
        items = cursor.fetchall()
        
        if not items:
            conn.close()
            return {"success": False, "message": "Order not found"}
        
        # Restore stock
        for product_id, quantity in items:
            cursor.execute('UPDATE Products SET stock_quantity = stock_quantity + ? WHERE product_id = ?',
                          (quantity, product_id))
        
        # Delete order items and order
        cursor.execute('DELETE FROM Order_Items WHERE order_id = ?', (order_id,))
        cursor.execute('DELETE FROM Orders WHERE order_id = ?', (order_id,))
        
        conn.commit()
        conn.close()
        
        return {"success": True, "message": f"Order {order_id} deleted successfully"}
        
    except Exception as e:
        conn.rollback()
        conn.close()
        return {"success": False, "message": f"Error deleting order: {str(e)}"}

def edit_order(order_id, status):
    """Edit order status"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if order exists
    cursor.execute('SELECT status FROM Orders WHERE order_id = ?', (order_id,))
    order = cursor.fetchone()
    
    if not order:
        conn.close()
        return {"success": False, "message": "Order not found"}
    
    # Update status
    cursor.execute('UPDATE Orders SET status = ? WHERE order_id = ?', (status, order_id))
    conn.commit()
    conn.close()
    
    return {"success": True, "message": f"Order {order_id} status updated to '{status}'"}

def show_orders(customer_id=None):
    """Show all orders or orders for specific customer"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if customer_id:
        cursor.execute('''
            SELECT o.order_id, c.first_name, c.last_name, o.order_date, o.total_amount, o.status
            FROM Orders o
            JOIN Customers c ON o.customer_id = c.customer_id
            WHERE o.customer_id = ?
            ORDER BY o.order_date DESC
        ''', (customer_id,))
    else:
        cursor.execute('''
            SELECT o.order_id, c.first_name, c.last_name, o.order_date, o.total_amount, o.status
            FROM Orders o
            JOIN Customers c ON o.customer_id = c.customer_id
            ORDER BY o.order_date DESC
        ''')
    
    orders = cursor.fetchall()
    conn.close()
    
    if not orders:
        return {"success": True, "orders": [], "message": "No orders found"}
    
    order_list = []
    for order in orders:
        order_list.append({
            "order_id": order[0],
            "customer": f"{order[1]} {order[2]}",
            "date": order[3],
            "total": order[4],
            "status": order[5]
        })
    
    return {"success": True, "orders": order_list, "count": len(order_list)}

def show_pending_orders():
    """Show only pending orders"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT o.order_id, c.first_name, c.last_name, o.order_date, o.total_amount
        FROM Orders o
        JOIN Customers c ON o.customer_id = c.customer_id
        WHERE o.status = 'pending'
        ORDER BY o.order_date DESC
    ''')
    
    orders = cursor.fetchall()
    conn.close()
    
    if not orders:
        return {"success": True, "orders": [], "message": "No pending orders found"}
    
    order_list = []
    for order in orders:
        order_list.append({
            "order_id": order[0],
            "customer": f"{order[1]} {order[2]}",
            "date": order[3],
            "total": order[4],
            "status": "pending"
        })
    
    return {"success": True, "orders": order_list, "count": len(order_list)}