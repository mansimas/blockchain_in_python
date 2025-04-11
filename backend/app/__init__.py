from flask import Flask, jsonify, request
import os, random, requests
from backend.blockchain.blockchain import Blockchain
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.pubsub import PubSub

app = Flask(__name__)
blockchain = Blockchain()
wallet = Wallet()
pubsub = PubSub(blockchain)

@app.route('/')
def route_default():
    return 'Hello, World!'

@app.route('/blockchain')
def route_blockchain():
    return jsonify(blockchain.to_json())

@app.route('/blockchain/mine')
def route_blockchain_mine():
    transaction_data = 'stubbed_transaction_data'
    blockchain.add_block(transaction_data)
    block = blockchain.chain[-1]
    pubsub.broadcast_block(block)
    return jsonify(block.to_json())

@app.route('/wallet/transact', methods=['POST'])
def route_wallet_transact():
    transaction_data = request.get_json()
    transaction = Transaction(wallet, transaction_data['recipient'], transaction_data['amount'])
    print(f'transaction {transaction.to_json()}')
    return jsonify(transaction.to_json())

ROOT_PORT = 5000
PORT = ROOT_PORT

if os.environ.get('PEER') == 'True':
    PORT = random.randint(5001, 6000)
    result = requests.get(f'http://localhost:{ROOT_PORT}/blockchain')
    result_blockchain = Blockchain.from_json(result.json())
    try:
        blockchain.replace_chain(result_blockchain.chain)
        print(f'\n -- Successfully replaced the local chain with the chain from peer')
    except Exception as e:
        print(f'\n -- Failed to replace chain: {e}')

app.run(port=PORT)