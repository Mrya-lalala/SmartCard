from flask import Flask, jsonify, request, send_from_directory
from smartcard import SmartCard

app = Flask(__name__)

# Homepage for API reference
@app.route("/", methods=["GET"])
def api_home():
    return jsonify({
        "message": "Smart Card API is live!",
        "endpoints": [
            "/card",
            "/card/<card_id>/topup",
            "/card/<card_id>/pay",
            "/card/<card_id>/balance",
            "/card/<card_id>/history"
        ]
    })

# Web interface route (dashboard)
@app.route("/dashboard", methods=["GET"])
def dashboard():
    return send_from_directory("static", "index.html")


# Create a new card
@app.route("/card", methods=["POST"])
def create_card():
    card_id = SmartCard.create_card()
    return jsonify({"message": "Card created", "card_id": card_id})

# Top up a card
@app.route("/card/<card_id>/topup", methods=["POST"])
def top_up(card_id):
    amount = request.json.get("amount")
    try:
        card = SmartCard(card_id)
        card.top_up(float(amount))
        return jsonify({"message": "Top-up successful", "new_balance": card.get_balance()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Pay for a meal
@app.route("/card/<card_id>/pay", methods=["POST"])
def pay_meal(card_id):
    cost = request.json.get("cost")
    try:
        card = SmartCard(card_id)
        card.pay_meal(float(cost))
        return jsonify({"message": "Payment successful", "new_balance": card.get_balance()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Check balance
@app.route("/card/<card_id>/balance", methods=["GET"])
def get_balance(card_id):
    try:
        card = SmartCard(card_id)
        return jsonify({"balance": card.get_balance()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Get transaction history
@app.route("/card/<card_id>/history", methods=["GET"])
def get_history(card_id):
    try:
        card = SmartCard(card_id)
        return jsonify({"transactions": card.get_history()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Run the app locally (not needed in production on Render)
if __name__ == "__main__":
    app.run(debug=True)
