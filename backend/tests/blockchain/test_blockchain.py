import pytest
from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import GENESIS_DATA

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
        blockchain.add_block(i)
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