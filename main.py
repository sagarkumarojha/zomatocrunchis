from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)
menu = []
orders = []


@app.route('/')
def hello():
    return 'Welcome to Zesty Zomato!'


@app.route('/menu', methods=['GET'])
def get_menu():
    return jsonify(menu)


@app.route('/menu', methods=['POST'])
def add_dish():
    # Retrieve the dish details from the request
    dish = {
        'id': request.json.get('id'),
        'name': request.json.get('name'),
        'price': request.json.get('price'),
        'availability': request.json.get('availability')
    }

    # Add the dish to the menu
    menu.append(dish)

    # Save the menu to the file
    save_data()

    # Return a success message
    return 'Dish added successfully!'


@app.route('/menu/<dish_id>', methods=['DELETE'])
def remove_dish(dish_id):
    # Find the dish with the given ID
    for dish in menu:
        if dish['id'] == dish_id:
            # Remove the dish from the menu
            menu.remove(dish)

            # Save the menu to the file
            save_data()

            return 'Dish removed successfully!'

    # Return an error message if the dish is not found
    return 'Dish not found!', 404


@app.route('/orders', methods=['POST'])
def take_order():
    # Retrieve the order details from the request
    customer_name = request.json.get('customer_name')
    dish_ids = request.json.get('dish_ids')

    # Check if all dishes are available
    for dish_id in dish_ids:
        dish = next((dish for dish in menu if dish['id'] == dish_id), None)
        if not dish or not dish['availability']:
            return 'Invalid order! One or more dishes are not available.', 400

    # Generate a unique order ID
    order_id = len(orders) + 1

    # Create the order dictionary
    order = {
        'order_id': order_id,
        'customer_name': customer_name,
        'dish_ids': dish_ids,
        'status': 'received'
    }

    # Add the order to the orders list
    orders.append(order)

    # Save the orders to the file
    save_data()

    # Return the order ID
    return f'Order placed successfully! Order ID: {order_id}'


@app.route('/orders/<order_id>', methods=['PUT'])
def update_order_status(order_id):
    # Retrieve the new status from the request
    new_status = request.json.get('status')

    # Find the order with the given ID
    order = next((order for order in orders if order['order_id'] == int(order_id)), None)
    if not order:
        return 'Order not found!', 404

    # Update the status of the order
    order['status'] = new_status

    # Save the orders to the file
    save_data()

    # Return a success message
    return 'Order status updated successfully!'


def save_data():
    with open('menu.pickle', 'wb') as file:
        pickle.dump(menu, file)
    with open('orders.pickle', 'wb') as file:
        pickle.dump(orders, file)


def load_data():
    global menu
    try:
        with open('menu.pickle', 'rb') as file:
            menu = pickle.load(file)
    except FileNotFoundError:
        menu = []

    global orders
    try:
        with open('orders.pickle', 'rb') as file:
            orders = pickle.load(file)
    except FileNotFoundError:
        orders = []


load_data()

if __name__ == '__main__':
    app.run()
