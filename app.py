from flask import Flask, request, jsonify
from transaction_data import get_transaction_data  # Import the function

app = Flask(__name__)

@app.route("/get_data", methods=["POST"])
def get_data():
  try:
    # Get the transaction hash from the request body (assuming JSON format)
    data = request.get_json()
    tx_hash = data.get("tx_hash")
    if not tx_hash:
      return jsonify({"error": "Missing transaction hash"}), 400

    data = get_transaction_data(tx_hash)
    if data:
      return jsonify(data)
    else:
      return jsonify({"error": "Failed to retrieve transaction data"}), 500
  except Exception as e:
    print(f"Error processing request: {e}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
  app.run(debug=True)  # Set debug=False for production
