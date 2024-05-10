import asyncio
import json

from flask import Flask, request, jsonify
from hexbytes import HexBytes
from flask_cors import CORS
from web3 import Web3
import psycopg2

from main import get_transaction_data  # Import the function
import telegram_msg_sender as tbot

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow CORS for all origins

RPC_URL = "https://rpc-testnet.escscan.com"  # Replace with your desired RPC URL
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


web3 = Web3(Web3.HTTPProvider('https://rpc.escscan.com'))


@app.route("/contract_whitelist_count", methods=["GET"])
def whitelist_count():
    try:
        with open('whitelist.json', 'r') as file:
            whitelist_abi = json.load(file)
        whitelist_contract = web3.eth.contract(address='0x9D0b3C95dfc5D6913679E9D3B11Cc3A294a35a6B', abi=whitelist_abi)
        count = whitelist_contract.functions.count().call()
        return jsonify({"whitelist_count": count})
    except Exception as e:
        print(f"Error fetching latest whitelist count: {e}")
        return jsonify({"error": "Failed to fetch whitelist count"}), 500


DATABASE_URI = "postgresql://db_owner:6TA9ZIaxstfw@ep-delicate-darkness-a171tmzs.ap-southeast-1.aws.neon.tech/mainnet?sslmode=require"


@app.route('/database_whitelist_count', methods=['GET'])
def get_database_whitelist_count():
    try:
        conn = psycopg2.connect(DATABASE_URI)
        cur = conn.cursor()

        # Execute SQL query to count rows in members table
        cur.execute("SELECT COUNT(*) FROM members")
        count = cur.fetchone()[0]

        cur.close()
        conn.close()

        return jsonify({'whitelist_count': count})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route("/telegram_bot", methods=["GET"])
def send_message():
    try:
        asyncio.run(tbot.send_message(chat_id=-4002790376, message="Txn Mismatch Found...."))
        return jsonify({'message_sent' : True})
    except Exception as e:
        print(f"Error sending message from telegram: {e}")
        return jsonify({"error": "Failed to send message from telegram"}), 500


web3_bsc = Web3(Web3.HTTPProvider('https://bsc-dataseed1.binance.org/'))
@app.route("/total_claimed_lp", methods=["GET"])
def get_total_claimed_lp():
    try:
        with open('tempLP.json', 'r') as file:
            tempLPAbi = json.load(file)
        tempLPContract = web3_bsc.eth.contract(address='0x581E080513d628FD1e0Fb396a5744418d78c624F', abi=tempLPAbi)
        count = tempLPContract.functions.totalClaimed().call()
        return jsonify({"total_claimed": count})
    except Exception as e:
        print(f"Error fetching latest total claimed: {e}")
        return jsonify({"error": "Failed to fetch total claimed"}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)  # Set debug=False for production
