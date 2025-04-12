import requests, time
from backend.wallet.wallet import Wallet

BASE_URL = 'http://localhost:5000'

def get_blockchain():
    return requests.get(f'{BASE_URL}/blockchain').json()

def get_blockchain_mine():
    return requests.get(f'{BASE_URL}/blockchain/mine').json()

def post_wallet_transact(recipient, amount):
    return requests.post(
        f'{BASE_URL}/wallet/transact', json={
            'recipient': recipient,
            'amount': amount
        }
    ).json()

def get_wallet_info():
    return requests.get(f'{BASE_URL}/wallet/info').json()

start_blockchain = get_blockchain()
print("Initial Blockchain:", start_blockchain)

recipient = Wallet().address
post_wallet_transact_1 = post_wallet_transact(recipient, 21)
print(f'\n post_wallet_transact_1: {post_wallet_transact_1}')

time.sleep(1)

post_wallet_transact_2 = post_wallet_transact(recipient, 13)
print(f'\n post_wallet_transact_2: {post_wallet_transact_2}')

time.sleep(1)

mined_block = get_blockchain_mine()
print(f'\n mined_block: {mined_block}')

wallet_info = get_wallet_info()
print(f'\n wallet_info: {wallet_info}')