import numpy as np
import spacy
import re
import json
import time
import random
import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# ------------------------- Forecasting Model -------------------------
def train_forecasting_model():
    print("\n--- Forecasting Model Results ---")
    np.random.seed(42)
    X = np.random.rand(100, 1) * 10
    y = 2 * X + 1 + np.random.randn(100, 1) * 0.5

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mse = np.mean((y_test - y_pred) ** 2)
    print("RMSE:", mse ** 0.5)
    print("MAE:", mean_absolute_error(y_test, y_pred))
    print("R2 Score:", r2_score(y_test, y_pred))
    return model

# ------------------------- Chatbot -------------------------
class ChatBot:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def classify_intent(self, message):
        doc = self.nlp(message.lower())
        lemmas = [token.lemma_ for token in doc]

        if any(greet in lemmas for greet in ["hi", "hello", "hey"]):
            return "greeting"
        if "order" in lemmas and any(word in lemmas for word in ["track", "status", "check", "where"]):
            return "track_order"
        if "forecast" in lemmas or "demand" in lemmas:
            return "demand_forecast"
        if "product" in lemmas or "info" in lemmas or "price" in lemmas:
            return "product_info"
        if "bye" in lemmas or "exit" in lemmas or "quit" in lemmas:
            return "goodbye"
        return "unknown"

    def extract_order_id(self, message):
        match = re.search(r"\b[A-Z0-9]{4,}\b", message.upper())
        return match.group() if match else None

    def respond(self, message):
        intent = self.classify_intent(message)
        if intent == "greeting":
            return "Hello! How can I help you with your supply chain today?"
        elif intent == "track_order":
            order_id = self.extract_order_id(message)
            if order_id:
                return f"Looking up order ID {order_id}... Status: in transit 🚚"
            return "Please provide your order ID so I can track it."
        elif intent == "demand_forecast":
            return "This week's forecast: 📊 12% increase in demand expected due to seasonal trends."
        elif intent == "product_info":
            return "We offer 500+ products. Please specify a product name or type for more details."
        elif intent == "goodbye":
            return "Goodbye! Feel free to return if you have more questions."
        return "I'm not sure I understood. Try asking about orders, products, or demand forecasts."

    def chat(self):
        print("\n--- AI Chatbot Ready --- (type 'exit' to quit)")
        while True:
            msg = input("You: ")
            if msg.strip().lower() in ["exit", "quit", "bye"]:
                print("Bot: Goodbye! 👋")
                break
            print("Bot:", self.respond(msg))

def run_chatbot():
    bot = ChatBot()
    bot.chat()

# ------------------------- IoT Feed Simulation -------------------------
def generate_sensor_feed():
    feed = {
        "timestamp": time.time(),
        "stock_level": random.randint(50, 150),
        "transit_status": random.choice(["in_transit", "delivered", "delayed"])
    }
    return json.dumps(feed)

def simulate_iot_feed(duration_seconds=20):
    print("\n--- IoT Feed Simulation ---")
    start = time.time()
    while time.time() - start < duration_seconds:
        feed = generate_sensor_feed()
        print(feed)
        time.sleep(5)

# ------------------------- Blockchain Simulation -------------------------
class Block:
    def __init__(self, index, previous_hash, data, timestamp=None):
        self.index = index
        self.timestamp = timestamp or time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

def simulate_blockchain():
    print("\n--- Blockchain Simulation ---")
    chain = []
    genesis_block = Block(0, "0", "Genesis Block")
    chain.append(genesis_block)

    for i in range(1, 4):
        block = Block(i, chain[-1].hash, f"Transaction {i}")
        chain.append(block)

    for block in chain:
        print(f"Block {block.index}: {block.hash}")

# ------------------------- Security Framework -------------------------
def pad(data):
    pad_length = AES.block_size - len(data) % AES.block_size
    return data + pad_length * chr(pad_length)

def unpad(data):
    pad_length = ord(data[-1])
    return data[:-pad_length]

def encrypt_message(message, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_message = pad(message)
    encrypted_bytes = cipher.encrypt(padded_message.encode('utf-8'))
    return base64.b64encode(encrypted_bytes).decode('utf-8')

def decrypt_message(encrypted_message, key):
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_bytes = base64.b64decode(encrypted_message)
    decrypted_padded = cipher.decrypt(encrypted_bytes).decode('utf-8')
    return unpad(decrypted_padded)

def run_security_demo():
    print("\n--- Security Framework ---")
    key = get_random_bytes(16)
    message = "Sensitive Supply Chain Data"
    encrypted = encrypt_message(message, key)
    print("Encrypted:", encrypted)
    decrypted = decrypt_message(encrypted, key)
    print("Decrypted:", decrypted)

# ------------------------- Main Menu -------------------------
def main():
    print("\nAI-Powered Supply Chain Management System")
    while True:
        print("\nSelect an option:")
        print("1. Run Forecasting Model")
        print("2. Start Chatbot")
        print("3. Simulate IoT Feed")
        print("4. Simulate Blockchain Ledger")
        print("5. Run Security Encryption")
        print("6. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            train_forecasting_model()
        elif choice == "2":
            run_chatbot()
        elif choice == "3":
            simulate_iot_feed()
        elif choice == "4":
            simulate_blockchain()
        elif choice == "5":
            run_security_demo()
        elif choice == "6":
            print("Exiting system...")
            break
        else:
            print("Invalid choice. Try again.")

# ✅ Correct name check here
if __name__ == "__main__":
    main()
