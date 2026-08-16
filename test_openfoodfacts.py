import requests


BASE_URL = "https://world.openfoodfacts.org/api/v3"

HEADERS = {
    "User-Agent": "InventoryManagementSystem/1.0 (elvis.chege@student.moringaschool.com)"
}


def get_product_by_barcode(barcode):
    url = f"{BASE_URL}/product/{barcode}"

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        if response.status_code == 404:
            return None

        response.raise_for_status()

        data = response.json()

        if data.get("status") != 1:
            return None

        product = data.get("product", {})

        return {
            "barcode": barcode,
            "product_name": product.get("product_name"),
            "brands": product.get("brands"),
            "ingredients_text": product.get("ingredients_text"),
            "nutriscore_grade": product.get("nutriscore_grade")
        }

    except requests.RequestException:
        return None