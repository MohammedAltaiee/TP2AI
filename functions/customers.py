import sqlite3

def get_connection():
    """Get database connection"""
    return sqlite3.connect('ecommerce.db')

def add_customer(first_name, last_name, email, address=None):
    """Add a new customer to the database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO Customers (first_name, last_name, email, address)
            VALUES (?, ?, ?, ?)
        ''', (first_name, last_name, email, address))
        
        customer_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {"success": True, "customer_id": customer_id, 
                "message": f"Customer '{first_name} {last_name}' added successfully"}
        
    except sqlite3.IntegrityError:
        conn.close()
        return {"success": False, "message": "Email already exists"}
    except Exception as e:
        conn.close()
        return {"success": False, "message": f"Error adding customer: {str(e)}"}

def remove_customer(customer_id):
    """Remove a customer from the database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Check if customer exists
        cursor.execute('SELECT first_name, last_name FROM Customers WHERE customer_id = ?', (customer_id,))
        customer = cursor.fetchone()
        
        if not customer:
            conn.close()
            return {"success": False, "message": "Customer not found"}
        
        # Check for existing orders
        cursor.execute('SELECT COUNT(*) FROM Orders WHERE customer_id = ?', (customer_id,))
        order_count = cursor.fetchone()[0]
        
        if order_count > 0:
            conn.close()
            return {"success": False, "message": "Cannot delete customer with existing orders"}
        
        # Remove customer (this will also remove cart items due to foreign key)
        cursor.execute('DELETE FROM Carts WHERE customer_id = ?', (customer_id,))
        cursor.execute('DELETE FROM Customers WHERE customer_id = ?', (customer_id,))
        
        conn.commit()
        conn.close()
        
        return {"success": True, "message": f"Customer '{customer[0]} {customer[1]}' removed successfully"}
        
    except Exception as e:
        conn.rollback()
        conn.close()
        return {"success": False, "message": f"Error removing customer: {str(e)}"}

def edit_customer(customer_id, first_name=None, last_name=None, email=None, address=None):
    """Edit customer details"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Check if customer exists
        cursor.execute('SELECT first_name, last_name, email, address FROM Customers WHERE customer_id = ?', 
                      (customer_id,))
        customer = cursor.fetchone()
        
        if not customer:
            conn.close()
            return {"success": False, "message": "Customer not found"}
        
        # Use existing values if new ones not provided
        new_first_name = first_name if first_name is not None else customer[0]
        new_last_name = last_name if last_name is not None else customer[1]
        new_email = email if email is not None else customer[2]
        new_address = address if address is not None else customer[3]
        
        cursor.execute('''
            UPDATE Customers 
            SET first_name = ?, last_name = ?, email = ?, address = ?
            WHERE customer_id = ?
        ''', (new_first_name, new_last_name, new_email, new_address, customer_id))
        
        conn.commit()
        conn.close()
        
        return {"success": True, "message": f"Customer {customer_id} updated successfully"}
        
    except sqlite3.IntegrityError:
        conn.close()
        return {"success": False, "message": "Email already exists"}
    except Exception as e:
        conn.close()
        return {"success": False, "message": f"Error updating customer: {str(e)}"}

def show_customers():
    """Show all customers"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT customer_id, first_name, last_name, email, address
        FROM Customers
        ORDER BY last_name, first_name
    ''')
    
    customers = cursor.fetchall()
    conn.close()
    
    if not customers:
        return {"success": True, "customers": [], "message": "No customers found"}
    
    customer_list = []
    for customer in customers:
        customer_list.append({
            "customer_id": customer[0],
            "first_name": customer[1],
            "last_name": customer[2],
            "email": customer[3],
            "address": customer[4]
        })
    
    return {"success": True, "customers": customer_list, "count": len(customer_list)}

def get_customer(customer_id):
    """Get specific customer details"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT customer_id, first_name, last_name, email, address
        FROM Customers
        WHERE customer_id = ?
    ''', (customer_id,))
    
    customer = cursor.fetchone()
    conn.close()
    
    if not customer:
        return {"success": False, "message": "Customer not found"}
    
    return {
        "success": True,
        "customer": {
            "customer_id": customer[0],
            "first_name": customer[1],
            "last_name": customer[2],
            "email": customer[3],
            "address": customer[4]
        }
    }