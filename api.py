#!/usr/bin/env python3
"""
Flask API server for eCommerce database
Run with: python api.py
Test endpoints with: curl or Postman
"""

from flask import Flask, request, jsonify
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'functions'))

from functions import products, carts, orders, customers, analyse
from create_db import create_database

app = Flask(__name__)

# Error handler
@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "message": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"success": False, "message": "Internal server error"}), 500

# Products endpoints
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products.show_products())

@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    return jsonify(products.add_product(
        data['name'], data['description'], data['price'], data['stock']
    ))

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    return jsonify(products.remove_product(product_id))

# Customers endpoints
@app.route('/customers', methods=['GET'])
def get_customers():
    return jsonify(customers.show_customers())

@app.route('/customers', methods=['POST'])
def add_customer():
    data = request.json
    return jsonify(customers.add_customer(
        data['first_name'], data['last_name'], data['email'], data.get('address')
    ))

@app.route('/customers/<int:customer_id>', methods=['PUT'])
def edit_customer(customer_id):
    data = request.json
    return jsonify(customers.edit_customer(
        customer_id, 
        data.get('first_name'), 
        data.get('last_name'), 
        data.get('email'), 
        data.get('address')
    ))

@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    return jsonify(customers.remove_customer(customer_id))

# Cart endpoints
@app.route('/cart/<int:customer_id>', methods=['GET'])
def get_cart(customer_id):
    return jsonify(carts.show_cart(customer_id))

@app.route('/cart/<int:customer_id>/add', methods=['POST'])
def add_to_cart(customer_id):
    data = request.json
    return jsonify(carts.add_to_cart(customer_id, data['product_id'], data['quantity']))

@app.route('/cart/<int:customer_id>/remove', methods=['POST'])
def remove_from_cart(customer_id):
    data = request.json
    return jsonify(carts.remove_from_cart(
        customer_id, data['product_id'], data.get('quantity')
    ))

@app.route('/cart/<int:customer_id>', methods=['DELETE'])
def clear_cart(customer_id):
    return jsonify(carts.drop_cart(customer_id))

# Orders endpoints
@app.route('/orders', methods=['GET'])
def get_orders():
    customer_id = request.args.get('customer_id', type=int)
    return jsonify(orders.show_orders(customer_id))

@app.route('/orders/pending', methods=['GET'])
def get_pending_orders():
    return jsonify(orders.show_pending_orders())

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    items = [(item['product_id'], item['quantity']) for item in data['items']]
    return jsonify(orders.create_order(data['customer_id'], items, data.get('status', 'pending')))

@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.json
    return jsonify(orders.edit_order(order_id, data['status']))

@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    return jsonify(orders.delete_order(order_id))

# Analytics endpoints
@app.route('/analytics/customers', methods=['GET'])
def get_customer_analytics():
    return jsonify(analyse.sorted_total_purchases())

@app.route('/analytics/products/top', methods=['GET'])
def get_top_products():
    n = request.args.get('n', 5, type=int)
    return jsonify(analyse.show_top_products(n))

@app.route('/analytics/products/bottom', methods=['GET'])
def get_bottom_products():
    n = request.args.get('n', 5, type=int)
    return jsonify(analyse.show_bottom_products(n))

@app.route('/analytics/summary', methods=['GET'])
def get_sales_summary():
    return jsonify(analyse.get_sales_summary())

# Utility endpoints
@app.route('/init-db', methods=['POST'])
def initialize_database():
    try:
        create_database()
        return jsonify({"success": True, "message": "Database initialized successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Database initialization failed: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"success": True, "message": "API is running", "status": "healthy"})

@app.route('/', methods=['GET'])
def api_info():
    return jsonify({
        "success": True,
        "message": "eCommerce API Server",
        "endpoints": {
            "products": ["GET /products", "POST /products", "DELETE /products/<id>"],
            "customers": ["GET /customers", "POST /customers", "PUT /customers/<id>", "DELETE /customers/<id>"],
            "cart": ["GET /cart/<customer_id>", "POST /cart/<customer_id>/add", "POST /cart/<customer_id>/remove", "DELETE /cart/<customer_id>"],
            "orders": ["GET /orders", "GET /orders/pending", "POST /orders", "PUT /orders/<id>", "DELETE /orders/<id>"],
            "analytics": ["GET /analytics/customers", "GET /analytics/products/top", "GET /analytics/products/bottom", "GET /analytics/summary"],
            "utility": ["POST /init-db", "GET /health"]
        }
    })

if __name__ == '__main__':
    print("Starting eCommerce API Server...")
    print("Available at: http://localhost:5000")
    print("API Documentation: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)