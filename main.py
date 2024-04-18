from hexbytes import HexBytes
from web3 import Web3
import json


def get_transaction_data(tx_hash):
    RPC_URL = "https://rpc-testnet.escscan.com"  # Replace with your desired RPC URL
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    try:
        transaction = w3.eth.get_transaction(tx_hash)
        receipt = w3.eth.get_transaction_receipt(tx_hash)
        # print(transaction)
        # print(receipt)

        data = {}
        data['blockNumber'] = receipt.blockNumber
        data['contractAddress'] = receipt.contractAddress
        data['cumulativeGasUsed'] = receipt.cumulativeGasUsed
        data['from'] = receipt['from']
        data['to'] = transaction.to
        data['gasUsed'] = receipt.gasUsed
        data['effectiveGasPrice'] = receipt.effectiveGasPrice
        data['chainId'] = transaction.chainId
        data['maxPriorityFeePerGas'] = transaction.maxPriorityFeePerGas

        print(data)
        return data
    except Exception as e:
        print(f"Error fetching transaction data: {e}")
        return None


# get_transaction_data(0x6c6266877c2ab742239f8183aac31b426bd0394d95c139faa63b1978ccfbd47b)
