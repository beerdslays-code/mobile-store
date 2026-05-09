import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import order_service
import payment_service
from supabase_client import get_supabase

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")


# --- DATABASE HELPERS ---

def get_products():
    """Fetch all game products from Supabase."""
    try:
        supabase = get_supabase()
        response = supabase.table("products").select("*").execute()
        return response.data or []
    except Exception as e:
        print(f"[DB ERROR] Could not fetch products: {e}")
        return []


def get_product_by_id(product_id: str):
    """Fetch a single game product by ID."""
    try:
        supabase = get_supabase()
        response = (
            supabase.table("products")
            .select("*")
            .eq("id", product_id)
            .single()
            .execute()
        )
        return response.data
    except Exception as e:
        print(f"[DB ERROR] Could not fetch product {product_id}: {e}")
        return None


# --- ROUTES ---

@app.route("/")
def index():
    products = get_products()
    return render_template("index.html", products=products)


@app.route("/order", methods=["POST"])
def place_order():
    data = request.get_json()

    try:
        product_id = data.get("product_id")
        quantity = int(data.get("quantity", 1))
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Invalid quantity."}), 400

    payment_method = data.get("payment_method", "gcash")
    customer_name  = data.get("customer_name", "").strip()
    customer_email = data.get("customer_email", "").strip()
    game_uid       = data.get("game_uid", "").strip()
    game_server    = data.get("game_server", "").strip()
    denom_label    = data.get("denom_label", "").strip()
    unit_price     = float(data.get("unit_price", 0))
    total_price    = float(data.get("total_price", unit_price * quantity))
    product_name   = data.get("product_name", "")

    # Validate product exists
    product = get_product_by_id(product_id)
    if not product:
        return jsonify({"success": False, "message": "Game not found."}), 404

    order_data = {
        "product_id":     product_id,
        "product_name":   product.get("name", product_name),
        "quantity":       quantity,
        "condition":      "original",
        "payment_method": payment_method,
        "unit_price":     unit_price,
        "total_price":    total_price,
        "customer_name":  customer_name,
        "customer_email": customer_email,
        "game_uid":       game_uid,
        "game_server":    game_server,
        "denom_label":    denom_label,
        "status":         "pending",
    }

    pay_result = payment_service.process_payment(order_data)
    if not pay_result["success"]:
        return jsonify({"success": False, "message": pay_result["message"]}), 400

    try:
        created = order_service.create_order(order_data)
        if created is None:
            return jsonify({
                "success": True,
                "message": pay_result["message"] + " (Demo mode — order not saved to DB)",
                "order": order_data,
            })
    except Exception as e:
        print(f"[ORDER ERROR] {e}")
        return jsonify({
            "success": True,
            "message": pay_result["message"] + " (Demo mode — check DB connection)",
            "order": order_data,
        })

    return jsonify({
        "success": True,
        "message": pay_result["message"],
        "order": created,
    })


@app.route("/orders")
def order_history():
    try:
        orders = order_service.get_all_orders()
    except Exception:
        orders = []
    return render_template("order_history.html", orders=orders)


@app.route("/api/products")
def api_products():
    return jsonify(get_products())


@app.route("/api/product/<product_id>")
def api_product(product_id):
    product = get_product_by_id(product_id)
    if not product:
        return jsonify({"error": "Not found"}), 404
    return jsonify(product)


if __name__ == "__main__":
    app.run(debug=True)