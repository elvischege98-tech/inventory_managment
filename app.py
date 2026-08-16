from flask import Flask, jsonify, request
from inventory import inventory

app = Flask(__name__)

@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory)

@app.route("/inventory/<int:item_id>",
methods=["GET"])
def get_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return jsonify(item)
        
    return jsonify({"error": "Item not found"}), 404


@app.route("/inventory/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid input"}), 400
    
    for item in inventory:
        if item["id"] == item_id:
           if "status" in data:
                item["status"] = data["status"]
           if "product" in data:
                item["product"] = data["product"]
           return jsonify(item),200
        
    return jsonify({"error": "Item not found"}), 404

@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            inventory.remove(item)
            return jsonify({"message": "Item deleted"}), 200
        
    return jsonify({"error": "Item not found"}), 404

@app.route("/inventory", methods=["POST"])
def add_item():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid input"}), 400
    
    required_fields = ["status", "product"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400
        
    new_id=max([item["id"] for item in inventory], default=0)+1

    new_item = {
        "id": new_id,
        "status": data["status"],
        "product": data["product"]
    }

    inventory.append(new_item)
    return jsonify(new_item), 201

if __name__ == '__main__':
    app.run(debug=True) 


