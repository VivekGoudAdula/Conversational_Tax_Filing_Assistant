import re
from data_store import parse_amount

def process_prompt(message, user_data):
    message = message.lower()

    # Friendly / small talk responses
    if any(word in message for word in ["hi", "hello", "hey"]):
        return "Hey there! 😊 I'm your tax assistant. You can start by telling me your income, expenses, or anything tax-related."
    
    if "hello" in message or "hi" in message:
        return "Hey there! Ready to dive into some numbers? 📊"

    if "help" in message:
        return "I'm here to assist you with anything tax-related. Just tell me what you need! 🧾"

    if "who are you" in message:
        return "I'm your digital tax assistant – your stress-free guide to filing taxes! 🤖💰"

    if "what can you do" in message:
        return "I can help generate reports, calculate taxes, and make your financial paperwork easier! 📋"

    if "joke" in message:
        return "Why don’t accountants ever get lost? Because they always follow the ledger! 😄"

    if "file my taxes" in message:
        return "Absolutely! Just provide me the necessary data and I’ll handle the rest. 🗃️"

    if "thanks a lot" in message or "appreciate it" in message:
        return "Happy to help! Filing taxes just got a little more fun. 🎉"

    if "you're slow" in message:
        return "Oops! My bad – crunching numbers can take a second. Thanks for your patience. 🐢💡"

    if "what is tax" in message:
        return "Taxes are contributions you pay to the government to fund public services. And yes, they’re kinda important! 🏛️"

    if "can you save my data" in message:
        return "For now, I don’t store data long-term – just enough to help you during this session. 🔐"

    if "okay" in message or "cool" in message:
        return "Great! Let’s keep things rolling. 😎"

    if "you're awesome" in message:
        return "Aww, thank you! You’re pretty awesome too. 🌟"

    if "not working" in message:
        return "Hmm... something seems off. Want to try again or get some help? 🛠️"

    if "let's start" in message:
        return "Awesome! Let's get you sorted out. Just share your info when you're ready. 🚀"

    # Actual financial info
    if "income" in message:
        amount = extract_amount(message)
        if amount: user_data["income"] += amount; return f"Income ₹{amount} added."

    elif "expense" in message:
        amount = extract_amount(message)
        if amount: user_data["expenses"].append(amount); return f"Expense ₹{amount} added."

    elif "investment" in message:
        amount = extract_amount(message)
        if amount: user_data["investments"].append(amount); return f"Investment ₹{amount} added."

    elif "capital gain" in message:
        amount = extract_amount(message)
        if amount: user_data["capital_gains"].append(amount); return f"Capital Gain ₹{amount} added."

    elif "loan" in message:
        amount = extract_amount(message)
        if amount: user_data["loans"].append(amount); return f"Loan ₹{amount} added."

    elif "gst" in message:
        amount = extract_amount(message)
        if amount: user_data["gst_inputs"].append(amount); return f"GST ₹{amount} added."

    return "Could you clarify your input? For example: 'I had ₹50,000 income' or 'I paid ₹10,000 as GST'."

def extract_amount(msg):
    match = re.search(r"(\d+(?:,?\d+)?[kKlL]?)", msg)
    if match:
        return parse_amount(match.group(1))
    return None

required_fields = ["income", "expenses", "investments", "capital_gains", "loans", "gst_inputs"]

def get_missing_fields(user_data):
    missing = []
    for field in required_fields:
        value = user_data.get(field, 0 if field == "income" else [])
        if (field == "income" and value == 0) or (isinstance(value, list) and not value):
            missing.append(field.replace("_", " ").title())
    return missing
