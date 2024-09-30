import hashlib
import time
import json
from flask import Flask, jsonify, request

class Block:
    def __init__(self, index, previous_hash, timestamp, data, token):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.token = token
        self.hash = self.hash_block()

    def hash_block(self):
        block_string = json.dumps({
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "data": self.data,
            "token": self.token
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block", "GENESIS_TOKEN")

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, data, token):
        previous_block = self.get_last_block()
        new_block = Block(len(self.chain), previous_block.hash, time.time(), data, token)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.hash_block():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

# API using Flask to interact with the blockchain
app = Flask(__name__)

blockchain = Blockchain()

@app.route('/mine_block', methods=['POST'])
def mine_block():
    data = request.json.get("data", "New transaction data")  # Lấy dữ liệu từ request
    token = request.json.get("token", "NEW_TOKEN")          # Lấy token từ request
    blockchain.add_block(data, token)
    return jsonify({
        "message": "Block mined",
        "index": blockchain.get_last_block().index,
        "previous_hash": blockchain.get_last_block().previous_hash,
        "hash": blockchain.get_last_block().hash,
        "data": blockchain.get_last_block().data,
        "token": blockchain.get_last_block().token
    })

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = [{"index": block.index,
                   "previous_hash": block.previous_hash,
                   "timestamp": block.timestamp,
                   "data": block.data,
                   "token": block.token,
                   "hash": block.hash} for block in blockchain.chain]
    return jsonify({
        "chain": chain_data,
        "length": len(chain_data)
    })

if __name__ == '__main__':
    app.run(debug=True)
