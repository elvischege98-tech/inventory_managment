from flask import Flask, jsonify, request
from inventory import inventory
import requests

app = Flask(__name__)

@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory)

@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return jsonify(item)
        
    return jsonify({"error": "Item not found"}), 404


@app.route("/product/<barcode>", methods=["GET"])
def get_product(barcode):
    url = f"https://world.openfoodfacts.org/api/v3/product/{barcode}"

    headers = {
        "User-Agent": "InventoryManagementSystem/1.0 (elvis.chege@student.moringaschool.com)"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        print("Status:", response.status_code)
        print("Response:", response.text[:500])

        if response.status_code == 404:
            return jsonify({
                "error": "Product not found",
                "barcode": barcode
            }), 404

        if response.status_code != 200:
            return jsonify({
                "error": "Open Food Facts API error",
                "status_code": response.status_code
            }), 502

        data = response.json()

    except requests.RequestException as e:
        return jsonify({
            "error": "Could not connect to Open Food Facts",
            "details": str(e)
        }), 502

    product = data.get("product", {})

    return jsonify({
        "barcode": barcode,
        "product_name": product.get("product_name"),
        "brands": product.get("brands"),
        "ingredients_text": product.get("ingredients_text"),
        "nutriscore_grade": product.get("nutriscore_grade") 
    }), 200



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


