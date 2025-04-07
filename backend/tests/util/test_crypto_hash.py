from backend.util.crypto_hash import crypto_hash

def test_crypto_hash():
  # it should create a SHA-256 hash of the given inputs by
  assert crypto_hash(1, [2], 'three') == crypto_hash('three', 1, [2])