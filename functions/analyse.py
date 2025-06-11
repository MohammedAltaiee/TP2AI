import sqlite3

def get_connection():
    """Get database connection"""
    return sqlite3.connect('ecommerce.db')

def sorted_total_purchases():
    """Get sorted total purchases for each client"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            c.customer_id,
            c.first_name,
            c.last_name,
            c.email,
            COALESCE(SUM(o.total_amount), 0) as total_purchases,
            COUNT(o.order_id) as order_count
        FROM Customers c
        LEFT JOIN Orders o ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.first_name, c.last_name, c.email
        ORDER BY total_purchases DESC
    ''')
    
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        return {"success": True, "customers": [], "message": "No customers found"}
    
    customer_purchases = []
    for row in results:
        customer_purchases.append({
            "customer_id": row[0],
            "name": f"{row[1]} {row[2]}",
            "email": row[3],
            "total_purchases": row[4],
            "order_count": row[5]
        })
    
    return {"success": True, "customers": customer_purchases, "count": len(customer_purchases)}

def show_top_products(n=5):
    """Show top N products by sales volume"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            p.product_id,
            p.product_name,
            p.price,
            COALESCE(SUM(oi.quantity), 0) as total_sold,
            COALESCE(SUM(oi.quantity * oi.unit_price), 0) as total_revenue
        FROM Products p
        LEFT JOIN Order_Items oi ON p.product_id = oi.product_id
        GROUP BY p.product_id, p.product_name, p.price
        ORDER BY total_sold DESC
        LIMIT ?
    ''', (n,))
    
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        return {"success": True, "products": [], "message": "No products found"}
    
    top_products = []
    for row in results:
        top_products.append({
            "product_id": row[0],
            "product_name": row[1],
            "price": row[2],
            "total_sold": row[3],
            "total_revenue": row[4]
        })
    
    return {"success": True, "products": top_products, "count": len(top_products), 
            "message": f"Top {n} products by sales volume"}

def show_bottom_products(n=5):
    """Show bottom N products by sales volume"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            p.product_id,
            p.product_name,
            p.price,
            COALESCE(SUM(oi.quantity), 0) as total_sold,
            COALESCE(SUM(oi.quantity * oi.unit_price), 0) as total_revenue
        FROM Products p
        LEFT JOIN Order_Items oi ON p.product_id = oi.product_id
        GROUP BY p.product_id, p.product_name, p.price
        ORDER BY total_sold ASC
        LIMIT ?
    ''', (n,))
    
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        return {"success": True, "products": [], "message": "No products found"}
    
    bottom_products = []
    for row in results:
        bottom_products.append({
            "product_id": row[0],
            "product_name": row[1],
            "price": row[2],
            "total_sold": row[3],
            "total_revenue": row[4]
        })
    
    return {"success": True, "products": bottom_products, "count": len(bottom_products), 
            "message": f"Bottom {n} products by sales volume"}

def get_sales_summary():
    """Get overall sales summary"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Total sales
    cursor.execute('SELECT COUNT(*), COALESCE(SUM(total_amount), 0) FROM Orders')
    total_orders, total_revenue = cursor.fetchone()
    
    # Average order value
    cursor.execute('SELECT COALESCE(AVG(total_amount), 0) FROM Orders')
    avg_order_value = cursor.fetchone()[0]
    
    # Most popular product
    cursor.execute('''
        SELECT p.product_name, SUM(oi.quantity) as total_sold
        FROM Products p
        JOIN Order_Items oi ON p.product_id = oi.product_id
        GROUP BY p.product_id, p.product_name
        ORDER BY total_sold DESC
        LIMIT 1
    ''')
    popular_product = cursor.fetchone()
    
    conn.close()
    
    return {
        "success": True,
        "summary": {
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "average_order_value": round(avg_order_value, 2),
            "most_popular_product": popular_product[0] if popular_product else "None",
            "most_popular_quantity": popular_product[1] if popular_product else 0
        }
    }