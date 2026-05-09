"""
payment_service.py
-------------------
Handles payment method validation and processing for GameTop.
In a real deployment, integrate PayMongo (PH) for GCash, cards, Maya, etc.
"""

PAYMENT_METHODS = {
    "gcash":          "GCash",
    "credit_card":    "Credit / Debit Card",
    "bank_transfer":  "Maya",
    "cash":           "Cash on Delivery",
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

    game    = order_data.get("product_name", "your game")
    denom   = order_data.get("denom_label", "selected pack")
    game_uid = order_data.get("game_uid", "")

    if method == "cash":
        return {
            "success": True,
            "message": f"Order placed! {denom} for {game} will be delivered to UID: {game_uid}.",
            "transaction_ref": None,
        }

    import uuid
    ref = str(uuid.uuid4())[:8].upper()
    label = PAYMENT_METHODS[method]
    return {
        "success": True,
        "message": f"Payment received via {label} (Ref: {ref}). {denom} will be sent to {game} UID: {game_uid} shortly!",
        "transaction_ref": ref,
    }