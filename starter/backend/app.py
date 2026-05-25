from flask import Flask, request, jsonify, send_from_directory
from backend.order_tracker import OrderTracker
from backend.in_memory_storage import InMemoryStorage

app = Flask(__name__, static_folder='../frontend')
in_memory_storage = InMemoryStorage()
order_tracker = OrderTracker(in_memory_storage)


@app.errorhandler(KeyError)
def handle_key_error(_: KeyError):
    return jsonify({"error": "Order not found"}), 404

@app.errorhandler(ValueError)
def handle_value_error(_: ValueError):
    return jsonify({"error": "Invalid data"}), 400

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/api/orders', methods=['POST'])
def add_order_api():
    data = request.get_json()
    order_tracker.add_order(**data)
    return jsonify(data), 201

@app.route('/api/orders/<string:order_id>', methods=['GET'])
def get_order_api(order_id):
    return jsonify(order_tracker.get_order_by_id(order_id=order_id))

@app.route('/api/orders/<string:order_id>/status', methods=['PUT'])
def update_order_status_api(order_id):
    data = request.get_json()
    new_status = data.get("new_status", "")
    order_tracker.update_order_status(
        order_id=order_id,
        new_status=new_status
    )
    order = order_tracker.get_order_by_id(order_id=order_id)
    return jsonify(order)

@app.route('/api/orders', methods=['GET'])
def list_orders_api():
    if ('status' in request.args):
        orders = order_tracker.list_orders_by_status(status=request.args.get('status'))
    else:
        orders = order_tracker.list_all_orders()
    return jsonify([
        order for _, order in orders.items()
    ])

@app.route('/api/orders/<string:order_id>', methods=['DELETE'])
def delete_order_api(order_id):
    return jsonify(order_tracker.delete_order(order_id=order_id))

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
