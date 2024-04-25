import json

from flask import Flask, request, jsonify
from hexbytes import HexBytes
from flask_cors import CORS
from web3 import Web3

from main import get_transaction_data  # Import the function

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow CORS for all origins

RPC_URL = "https://rpc.escscan.com"  # Replace with your desired RPC URL
w3 = Web3(Web3.HTTPProvider(RPC_URL))

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

@app.route("/latest_block", methods=["GET"])
def latest_block():
    try:
        block_number = w3.eth.block_number
        return jsonify({"block_number": block_number})
    except Exception as e:
        print(f"Error fetching latest block number: {e}")
        return jsonify({"error": "Failed to fetch latest block number"}), 500

@app.route("/whitelist_count", methods=["GET"])
def whitelist_count():
    try:
        with open('./whitelist.json', 'r') as file:
            whitelist_abi = json.load(file)
        whitelist_contract = w3.eth.contract(address='0x275b493afbb4E9A6efC853807B897Fd8123F4ADd', abi=whitelist_abi)
        count = whitelist_contract.functions.count().call()
        return jsonify({"whitelist_count": count})
    except Exception as e:
        print(f"Error fetching latest whitelist count: {e}")
        return jsonify({"error": "Failed to fetch whitelist count"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)  # Set debug=False for production
