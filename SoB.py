import os
import json
import hashlib
import time

DIFFICULTY_TARGET = "0000ffff00000000000000000000000000000000000000000000000000000000"

def validate_transaction(transaction):
    if 'txid' not in transaction or 'fee' not in transaction or 'size' not in transaction:
        return False

    if transaction['fee'] < 0 or transaction['size'] < 0:
        return False
    return True

def mine_block(transactions):
    nonce = 0
    while True:
        block_data = json.dumps(transactions) + str(nonce)
        block_hash = hashlib.sha256(block_data.encode()).hexdigest()
        if block_hash < DIFFICULTY_TARGET:
            return nonce
        nonce += 1

def serialize_transaction(transaction):
    return json.dumps(transaction)

def main():
    mempool_folder = 'Pyhton Varios/code-challenge-2024-ClaudioGlez21/mempool/'
    transactions = []
    for filename in os.listdir(mempool_folder):
        with open(os.path.join(mempool_folder, filename), 'r') as file:
            transaction_data = json.load(file)
            if validate_transaction(transaction_data):
                transactions.append(transaction_data)

    coinbase_transaction = {'txid': 'coinbase', 'fee': 0, 'size': 0}  # Placeholder, replace with actual coinbase transaction
    nonce = mine_block([coinbase_transaction] + transactions)
    serialized_coinbase = serialize_transaction(coinbase_transaction)
    serialized_transactions = [serialize_transaction(tx) for tx in transactions]

    with open('output.txt', 'w') as output_file:
        output_file.write(f"Block Header: {nonce}\n")  # For simplicity, using nonce as block header
        output_file.write(f"Serialized Coinbase Transaction: {serialized_coinbase}\n")
        for tx in serialized_transactions:
            output_file.write(f"{tx}\n")

if __name__ == "__main__":
    main()
