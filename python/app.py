import hashlib
import time
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

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

# Tạo một blockchain mới
blockchain = Blockchain()

@app.route('/mine_block', methods=['POST'])
def mine_block():
    request_data = request.get_json()
    data = request_data.get("data")
    token = request_data.get("token")

    blockchain.add_block(data, token)
    return jsonify({
        "message": "Khối đã được khai thác!",
        "index": blockchain.get_last_block().index,
        "hash": blockchain.get_last_block().hash
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
