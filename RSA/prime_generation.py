#%%
from secrets import randbits
from random import randint
#Some code and ideas from https://medium.com/@prudywsh/how-to-generate-big-prime-numbers-miller-rabin-49e6e6af32fb
#%%

def fermats_test(prime : int, num_checks : int = 128):
  for i in range(num_checks):
    witness = randint(1,prime-1)
    primelike_property = pow(witness,prime-1,prime) == 1
    if not primelike_property:
      return False
  return True

def generate_prime_candiate_by_bit_length(bit_length : int) -> int:
  p = randbits(bit_length)
  p |= (1 << bit_length - 1) | 1
  return p 

def generate_prime_candiate_with_range(a : int, b:int) -> int:
  p = randint(a,b)
  p |= (1 << p.bit_length() - 1) | 1
  return p 

def generate_prime_by_bit_length(bit_length):

  while True:
    candidate = generate_prime_candiate_by_bit_length(bit_length)
    is_prime = fermats_test(candidate)
    if is_prime:
      return candidate

def generate_prime_with_range(a : int, b : int):

  while True:
    candidate = generate_prime_candiate_with_range(a,b)
    is_prime = fermats_test(candidate)
    if is_prime:
      return candidate

def generate_p_q(product_length : int):
  """
  n = p * q
  n_length = 1 + (q_bit_length - 1) +(p_bit_length - 1)
  q_bit_length = p_bit_length = n_length + 1 / 2
  """
  prime_length = product_length//2
  p = generate_prime_by_bit_length(prime_length + 1)
  q = generate_prime_by_bit_length(prime_length)
  return p, q


if __name__ == '__main__':
  p,q = generate_p_q(1000)
  n = p * q
  print(p, q,n)
  print(n.bit_length())
# %%
