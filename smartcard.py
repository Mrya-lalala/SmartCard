import json
import uuid
from datetime import datetime

DATA_FILE = 'data.json'

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

class SmartCard:
    def __init__(self, card_id):
        self.card_id = card_id
        self.data = load_data()
        if card_id not in self.data:
            raise ValueError("Card not found")

    @classmethod
    def create_card(cls):
        card_id = str(uuid.uuid4())
        data = load_data()
        data[card_id] = {
            "balance": 0.0,
            "transactions": []
        }
        save_data(data)
        return card_id

    def top_up(self, amount):
        self.data[self.card_id]['balance'] += amount
        self.data[self.card_id]['transactions'].append({
            "type": "top-up",
            "amount": amount,
            "date": str(datetime.now())
        })
        save_data(self.data)

    def pay_meal(self, cost):
        if self.data[self.card_id]['balance'] < cost:
            raise ValueError("Insufficient balance")
        self.data[self.card_id]['balance'] -= cost
        self.data[self.card_id]['transactions'].append({
            "type": "meal",
            "amount": -cost,
            "date": str(datetime.now())
        })
        save_data(self.data)

    def get_balance(self):
        return self.data[self.card_id]['balance']

    def get_history(self):
        return self.data[self.card_id]['transactions']
