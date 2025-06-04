from flask import Flask, jsonify, request
from smartcard import SmartCard

app = Flask(__name__)

from flask import Flask, jsonify

app = Flask(__name__)

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

# existing routes follow.. 

@app.route("/", methods=["GET"])
def home():
    return "<h1>Smart Card API is running</h1><p>Use the /card endpoint to start.</p>"

@app.route("/card", methods=["POST"])
def create_card():
    card_id = SmartCard.create_card()
    return jsonify({"message": "Card created", "card_id": card_id})

@app.route("/card/<card_id>/topup", methods=["POST"])
def top_up(card_id):
    amount = request.json.get("amount")
    try:
        card = SmartCard(card_id)
        card.top_up(float(amount))
        return jsonify({"message": "Top-up successful", "new_balance": card.get_balance()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/card/<card_id>/pay", methods=["POST"])
def pay_meal(card_id):
    cost = request.json.get("cost")
    try:
        card = SmartCard(card_id)
        card.pay_meal(float(cost))
        return jsonify({"message": "Payment successful", "new_balance": card.get_balance()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/card/<card_id>/balance", methods=["GET"])
def get_balance(card_id):
    try:
        card = SmartCard(card_id)
        return jsonify({"balance": card.get_balance()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/card/<card_id>/history", methods=["GET"])
def get_history(card_id):
    try:
        card = SmartCard(card_id)
        return jsonify({"transactions": card.get_history()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
