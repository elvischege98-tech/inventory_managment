import requests

BASE_URL = "http://127.0.0.1:5000"


def get_inventory():
    response = requests.get(f"{BASE_URL}/inventory")

    if response.status_code == 200:
        items = response.json()

        if not items:
            print("\nInventory is empty.")
            return

        print("\n===== INVENTORY =====")

        for item in items:
            print(f"ID: {item['id']}")
            print(f"Status: {item['status']}")
            print(f"Product: {item['product']}")
            print("--------------------")

    else:
        print("Error:", response.status_code)


def get_item():
    item_id = input("Enter item ID: ")

    response = requests.get(
        f"{BASE_URL}/inventory/{item_id}"
    )

    if response.status_code == 200:
        print("\n===== ITEM =====")
        print(response.json())

    else:
        print("\nError:", response.json())


def add_item():
    status = input("Enter status: ")
    product_name = input("Enter product name: ")
    brands = input("Enter brand: ")
    ingredients = input("Enter ingredients: ")

    data = {
        "status": int(status),
        "product": {
            "product_name": product_name,
            "brands": brands,
            "ingredients_text": ingredients
        }
    }

    response = requests.post(
        f"{BASE_URL}/inventory",
        json=data
    )

    if response.status_code == 201:
        print("\nItem added successfully!")
        print(response.json())

    else:
        print("\nError:", response.json())


def update_item():
    item_id = input("Enter item ID: ")

    status = input(
        "Enter new status (press Enter to keep current): "
    )

    product_name = input(
        "Enter new product name (press Enter to keep current): "
    )

    data = {}

    if status:
        data["status"] = int(status)

    if product_name:
        data["product"] = {
            "product_name": product_name
        }

    if not data:
        print("Nothing to update.")
        return

    response = requests.patch(
        f"{BASE_URL}/inventory/{item_id}",
        json=data
    )

    if response.status_code == 200:
        print("\nItem updated successfully!")
        print(response.json())

    else:
        print("\nError:", response.json())


def delete_item():
    item_id = input("Enter item ID: ")

    response = requests.delete(
        f"{BASE_URL}/inventory/{item_id}"
    )

    if response.status_code == 200:
        print("\nItem deleted successfully!")

    else:
        print("\nError:", response.json())


def find_product():
    barcode = input("Enter product barcode: ")

    response = requests.get(
        f"{BASE_URL}/product/{barcode}"
    )

    if response.status_code == 200:
        product = response.json()

        print("\n===== OPEN FOOD FACTS =====")
        print(f"Barcode: {product.get('barcode')}")
        print(f"Product: {product.get('product_name')}")
        print(f"Brand: {product.get('brands')}")
        print(f"Ingredients: {product.get('ingredients_text')}")
        print(f"Nutri-Score: {product.get('nutriscore_grade')}")

    else:
        print("\nError:", response.json())


def main():
    while True:

        print("\n")
        print("==============================")
        print("   INVENTORY MANAGEMENT CLI")
        print("==============================")
        print("1. View all inventory")
        print("2. Find inventory item")
        print("3. Add inventory item")
        print("4. Update inventory item")
        print("5. Delete inventory item")
        print("6. Find product by barcode")
        print("7. Exit")
        print("==============================")

        choice = input("Choose an option: ")

        if choice == "1":
            get_inventory()

        elif choice == "2":
            get_item()

        elif choice == "3":
            add_item()

        elif choice == "4":
            update_item()

        elif choice == "5":
            delete_item()

        elif choice == "6":
            find_product()

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()