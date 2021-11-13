#%%
from dataclasses import dataclass
from math import lcm
from num_theory import modular_inverse
from prime_generation import generate_p_q, generate_prime_with_range

#%%

@dataclass
class PublicKey:
  n : int
  e : int

  def key_length(self):
    return self.n.bit_length()

@dataclass
class PrivateKey:
  n : int
  d : int

  def key_length(self):
    return self.n.bit_length()


def generate_keys(key_length):
  have_generated_good_p_q = False
  p,q,lam = -1,-1,-1
  while  not have_generated_good_p_q:
    p , q = generate_p_q(key_length)
    n = p*q 
    lam = lcm((p-1),(q-1))
    have_generated_good_p_q = max(p,q) != lam

  d = generate_prime_with_range(max(p,q),lam)
  e = modular_inverse(d,lam)
  return PublicKey(n,e), PrivateKey(n,d)

def encrypt(m: int, public_key : PublicKey) -> int:
  assert(0 <= m < public_key.n)
  # "direct" method
  ciphertext = pow(m,public_key.e, public_key.n)
  return ciphertext

def decrypt(c: int, private_key : PrivateKey) -> int:
  message = pow(c, private_key.d, private_key.n)
  return message

# %%
if __name__ == '__main__':
  public, private = generate_keys(19) #2048
  print(public, private)
  m = 42069
  ciphertext = encrypt(m,public)
  m_new = decrypt(ciphertext, private)
  print(m,ciphertext,m_new)