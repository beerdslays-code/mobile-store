"""
payment_service.py
-------------------
Handles payment method validation and processing for Pison Phone Store.
In a real deployment, integrate PayMongo (PH) for GCash, cards, Maya, etc.
"""

PAYMENT_METHODS = {
    "gcash":         "GCash",
    "credit_card":   "Credit / Debit Card",
    "bank_transfer": "Maya",
    "cash":          "Cash on Delivery",
}


def get_payment_methods() -> dict:
    return PAYMENT_METHODS


def validate_payment_method(method: str) -> bool:
    return method in PAYMENT_METHODS


def calculate_total(unit_price: float, quantity: int) -> float:
    return round(unit_price * quantity, 2)


def process_payment(order_data: dict) -> dict:
    """
    Simulate payment processing.
    Replace with PayMongo or Dragonpay integration for production.
    """
    method = order_data.get("payment_method", "")
    if not validate_payment_method(method):
        return {"success": False, "message": "Invalid payment method.", "transaction_ref": None}

    product  = order_data.get("product_name", "your phone")
    variant  = order_data.get("denom_label", "")
    customer = order_data.get("customer_name", "")
    address  = order_data.get("game_server", "")

    variant_str = f" ({variant})" if variant else ""

    if method == "cash":
        return {
            "success": True,
            "message": f"Order placed! {product}{variant_str} will be delivered to {address}. Pay ₱{order_data.get('total_price', 0):,.2f} upon arrival.",
            "transaction_ref": None,
        }

    import uuid
    ref = str(uuid.uuid4())[:8].upper()
    label = PAYMENT_METHODS[method]
    return {
        "success": True,
        "message": f"Payment confirmed via {label} (Ref: {ref}). Your {product}{variant_str} will be shipped to {address} within 1–3 business days.",
        "transaction_ref": ref,
    }