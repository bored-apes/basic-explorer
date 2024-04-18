from flask import Flask, request, jsonify
from hexbytes import HexBytes
from flask_cors import CORS

from main import get_transaction_data  # Import the function

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow CORS for all origins


@app.route("/get_data", methods=["POST"])
def get_data():
  try:
    # Get the transaction hash from the request body (assuming JSON format)
    data = request.get_json()
    tx_hash = data.get("tx_hash")
    if not tx_hash:
      return jsonify({"error": "Missing transaction hash"}), 400

    transaction_data = get_transaction_data(tx_hash)
    if transaction_data:
      # Convert HexBytes objects to strings before serialization
      for key, value in transaction_data.items():
        if isinstance(value, HexBytes):
          transaction_data[key] = str(value)
      return jsonify(transaction_data)
    else:
      return jsonify({"error": "Failed to retrieve transaction data"}), 500
  except Exception as e:
    print(f"Error processing request: {e}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
  app.run(debug=True)  # Set debug=False for production
