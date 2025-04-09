from backend.blockchain.block import Block

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

def main():
  blockchain = Blockchain()
  blockchain.add_block("Transaction 1")
  blockchain.add_block("Transaction 2")
  blockchain.add_block("Transaction 3")
  print(blockchain)

if __name__ == '__main__':
  main()