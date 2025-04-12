from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction
from backend.config import MINING_REWARD_INPUT
from backend.wallet.wallet import Wallet

class Blockchain:
  """
  Blockchain: a public ledger of transactions.
  Implemented as a list of blocks - data sets of transactions.
  """

  def __init__(self):
    self.chain = [Block.genesis()]

  def add_block(self, data):
    self.chain.append(Block.mine_block(self.chain[-1], data))

  def __repr__(self):
    return f'Blockchain({self.chain})'
  
  def replace_chain(self, chain):
    """
    Replace the current chain with the incoming chain if the following rules apply:
    1. The incoming chain must be longer than the current chain
    2. The incoming chain must be valiformatted properly
    """
    if len(chain) <= len(self.chain):
      raise Exception('Incoming chain must be longer than current chain')

    try:
      Blockchain.is_valid_chain(chain)
    except Exception as e:
      raise Exception(f'Invalid incoming chain: {e}')

    self.chain = chain

  def to_json(self):
    """
    Serialize the blockchain into a list of blocks
    """
    return list(map(lambda block: block.to_json(), self.chain))
  
  @staticmethod
  def from_json(chain_json):
    """
    Deserialize the blockchain from a list of blocks
    The result will contain a chain list of Block objects
    """
    blockchain = Blockchain()
    blockchain.chain = list(map(lambda block_json: Block.from_json(block_json), chain_json))
    return blockchain

  @staticmethod
  def is_valid_chain(chain):
    """
    Validate the incoming chain
    Enforce the following rules of the blockchain:
    1. The chain must start with the genesis block
    2. Blocks must be formatted correctly
    """

    if chain[0] != Block.genesis():
      raise Exception('Genesis block is not first block in the chain')

    for i in range(1, len(chain)):
      block = chain[i]
      last_block = chain[i - 1]
      Block.is_valid_block(last_block, block)
    
    Blockchain.is_valid_transaction_chain(chain)
    
  @staticmethod
  def is_valid_transaction_chain(chain):
    """
    Enforce the rules of a chain composed of blocks of transactions.
    - Each transaction must only appear once in the chain.
    - There can only be one mining reward per block.
    - Each transaction must be valid.
    """

    transaction_ids = set()

    for i in range(len(chain)):
      block = chain[i]
      has_mining_reward = False

      for transaction_json in block.data:
        transaction = Transaction.from_json(transaction_json)

        if transaction.id in transaction_ids:
          raise Exception(f'Transaction {transaction.id} appears more than once in the chain')
        transaction_ids.add(transaction.id)

        if transaction.input == MINING_REWARD_INPUT:
          if has_mining_reward:
            raise Exception(f'Block contains more than one mining reward. Check block with hash: {block.hash}')
          has_mining_reward = True
        else:
          historic_blockchain = Blockchain()
          historic_blockchain.chain = chain[0:i]
          historic_balance = Wallet.calculate_balance(
            historic_blockchain,
            transaction.input['address']
          )
          if historic_balance != transaction.input['amount']:
            raise Exception(f'Transaction {transaction.id} has an invalid amount. Check block with hash: {block.hash}')
      
        Transaction.is_valid_transaction(transaction)

def main():
  blockchain = Blockchain()
  blockchain.add_block("Transaction 1")
  blockchain.add_block("Transaction 2")
  blockchain.add_block("Transaction 3")
  print(blockchain)

if __name__ == '__main__':
  main()