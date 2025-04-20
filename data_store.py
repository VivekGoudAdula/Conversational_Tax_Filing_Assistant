import os
import json

def load_user_data(username):
    path = f"users/{username}.json"
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return {
        "income": 0,
        "expenses": [],
        "investments": [],
        "capital_gains": [],
        "loans": [],
        "gst_inputs": []
    }

def save_user_data(username, data):
    with open(f"users/{username}.json", 'w') as f:
        json.dump(data, f)

def parse_amount(val):
    val = val.replace(',', '').lower()
    if 'k' in val:
        return float(val.replace('k', '')) * 1000
    elif 'l' in val:
        return float(val.replace('l', '')) * 100000
    return float(val)
