#!/usr/bin/env python3
"""
Main testing script for eCommerce database functions
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'functions'))

from functions import products, carts, orders, customers, analyse
from create_db import create_database

def print_result(result, title="Result"):
    """Pretty print results"""
    print(f"\n=== {title} ===")
    if result.get('success'):
        print("✓ SUCCESS")
        if 'message' in result:
            print(f"Message: {result['message']}")
        
        # Print data based on type
        if 'products' in result:
            for product in result['products']:
                print(f"- {product}")
        elif 'customers' in result:
            for customer in result['customers']:
                print(f"- {customer}")
        elif 'orders' in result:
            for order in result['orders']:
                print(f"- {order}")
        elif 'cart' in result:
            for item in result['cart']:
                print(f"- {item}")
            if 'total' in result:
                print(f"Cart Total: ${result['total']}")
        elif 'summary' in result:
            print(f"Summary: {result['summary']}")
    else:
        print("✗ FAILED")
        print(f"Error: {result.get('message', 'Unknown error')}")

def test_products():
    """Test product functions"""
    print("\n" + "="*50)
    print("TESTING PRODUCTS MODULE")
    print("="*50)
    
    # Show initial products
    print_result(products.show_products(), "Initial Products")
    
    # Add a new product
    print_result(products.add_product("Webcam", "HD webcam for video calls", 59.99, 20), "Add Webcam")
    
    # Show products after addition
    print_result(products.show_products(), "Products After Addition")
    
    # Remove a product (remove webcam - should be product_id 6)
    print_result(products.remove_product(6), "Remove Webcam")

def test_customers():
    """Test customer functions"""
    print("\n" + "="*50)
    print("TESTING CUSTOMERS MODULE")
    print("="*50)
    
    # Show initial customers
    print_result(customers.show_customers(), "Initial Customers")
    
    # Add a new customer
    print_result(customers.add_customer("Alice", "Brown", "alice.brown@email.com", "321 Elm St"), "Add Alice")
    
    # Edit customer
    print_result(customers.edit_customer(4, address="456 Maple Ave"), "Edit Alice's Address")
    
    # Show customers after changes
    print_result(customers.show_customers(), "Customers After Changes")

def test_carts():
    """Test cart functions"""
    print("\n" + "="*50)
    print("TESTING CARTS MODULE")
    print("="*50)
    
    # Show Alice's cart (customer_id 4)
    print_result(carts.show_cart(4), "Alice's Initial Cart")
    
    # Add items to cart
    print_result(carts.add_to_cart(4, 1, 1), "Add Laptop to Alice's Cart")
    print_result(carts.add_to_cart(4, 2, 2), "Add 2 Mice to Alice's Cart")
    
    # Show cart after additions
    print_result(carts.show_cart(4), "Alice's Cart After Additions")
    
    # Remove some items
    print_result(carts.remove_from_cart(4, 2, 1), "Remove 1 Mouse from Cart")
    
    # Show final cart
    print_result(carts.show_cart(4), "Alice's Final Cart")

def test_orders():
    """Test order functions"""
    print("\n" + "="*50)
    print("TESTING ORDERS MODULE")
    print("="*50)
    
    # Show initial orders
    print_result(orders.show_orders(), "All Orders")
    
    # Create new order for Alice (customer_id 4)
    items = [(3, 1), (5, 1)]  # 1 Keyboard + 1 Headphones
    print_result(orders.create_order(4, items), "Create Order for Alice")
    
    # Show orders after creation
    print_result(orders.show_orders(), "Orders After Creation")
    
    # Show pending orders
    print_result(orders.show_pending_orders(), "Pending Orders")
    
    # Edit order status
    print_result(orders.edit_order(4, "shipped"), "Update Order Status")
    
    # Show Alice's orders
    print_result(orders.show_orders(4), "Alice's Orders")

def test_analytics():
    """Test analytics functions"""
    print("\n" + "="*50)
    print("TESTING ANALYTICS MODULE")
    print("="*50)
    
    # Customer purchase analysis
    print_result(analyse.sorted_total_purchases(), "Customer Purchase Totals")
    
    # Top products
    print_result(analyse.show_top_products(3), "Top 3 Products")
    
    # Bottom products
    print_result(analyse.show_bottom_products(3), "Bottom 3 Products")
    
    # Sales summary
    print_result(analyse.get_sales_summary(), "Sales Summary")

def main():
    """Main test function"""
    print("="*60)
    print("ECOMMERCE DATABASE TESTING SUITE")
    print("="*60)
    
    # Create/reset database
    print("Creating database...")
    create_database()
    print("Database created successfully!")
    
    # Run all tests
    test_products()
    test_customers()
    test_carts()
    test_orders()
    test_analytics()
    
    print("\n" + "="*60)
    print("ALL TESTS COMPLETED")
    print("="*60)

if __name__ == "__main__":
    main()