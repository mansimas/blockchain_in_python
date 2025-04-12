import pytest
from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import GENESIS_DATA
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet

def test_blockchain_instance():
    blockchain = Blockchain()
    assert blockchain.chain[0].hash == GENESIS_DATA['hash']

def test_add_block():
    blockchain = Blockchain()
    data = 'test-data'
    blockchain.add_block(data)
    assert blockchain.chain[-1].data == data

@pytest.fixture
def blockchain_in_three_blocks():
    blockchain = Blockchain()
    for i in range(3):
        blockchain.add_block([Transaction(Wallet(), 'recipient', i).to_json()])
    return blockchain

def test_is_valid_chan(blockchain_in_three_blocks):
    Blockchain.is_valid_chain(blockchain_in_three_blocks.chain)

def test_is_valid_chain_bad_genesis(blockchain_in_three_blocks):
    blockchain_in_three_blocks.chain[0].hash = 'bad_hash'
    with pytest.raises(Exception, match='Genesis block is not first block in the chain'):
        Blockchain.is_valid_chain(blockchain_in_three_blocks.chain)

def test_replace_chain(blockchain_in_three_blocks):
    blockchain = Blockchain()
    blockchain.replace_chain(blockchain_in_three_blocks.chain)
    assert blockchain.chain == blockchain_in_three_blocks.chain

def test_replace_chain_not_longer(blockchain_in_three_blocks):
    blockchain = Blockchain()
    with pytest.raises(Exception, match='Incoming chain must be longer than current chain'):
        blockchain_in_three_blocks.replace_chain(blockchain.chain)

def test_replace_chain_bad_chain(blockchain_in_three_blocks):
    blockchain = Blockchain()
    blockchain_in_three_blocks.chain[1].hash = 'bad_hash'
    with pytest.raises(Exception, match='Invalid incoming chain'):
        blockchain.replace_chain(blockchain_in_three_blocks.chain)

def test_valid_transaction_chain(blockchain_in_three_blocks):
    Blockchain.is_valid_transaction_chain(blockchain_in_three_blocks.chain)

def test_is_valid_transaction_chain_duplicate_transactions(blockchain_in_three_blocks):
    transaction = Transaction(Wallet(), 'recipient', 1).to_json()
    blockchain_in_three_blocks.add_block([transaction, transaction])
    with pytest.raises(Exception, match='appears more than once in the chain'):
        Blockchain.is_valid_transaction_chain(blockchain_in_three_blocks.chain)

def test_is_valid_transaction_chain_multiple_rewards(blockchain_in_three_blocks):
    reward_1 = Transaction.reward_transaction(Wallet()).to_json()
    reward_2 = Transaction.reward_transaction(Wallet()).to_json()
    blockchain_in_three_blocks.add_block([reward_1, reward_2])
    with pytest.raises(Exception, match='Block contains more than one mining reward'):
        Blockchain.is_valid_transaction_chain(blockchain_in_three_blocks.chain)

def test_is_valid_transaction_chain_bad_transaction(blockchain_in_three_blocks):
    bad_transaction = Transaction(Wallet(), 'recipient', 1)
    bad_transaction.input['signature'] = Wallet().sign(bad_transaction.output)
    blockchain_in_three_blocks.add_block([bad_transaction.to_json()])
    with pytest.raises(Exception):
        Blockchain.is_valid_transaction_chain(blockchain_in_three_blocks.chain)
