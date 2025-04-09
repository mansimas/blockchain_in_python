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
  
  @staticmethod
  def is_valid_chain(chain):
    """
    Validate the incoming chain
    Enforce the following rules of the blockchain:
    1. The chain must start with the genesis block
    2. Blocks must be formatted correctly
    """

    if chain[0].__dict__ != Block.genesis().__dict__:
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