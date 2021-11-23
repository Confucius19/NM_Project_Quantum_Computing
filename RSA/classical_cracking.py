#%%
from math import lcm
from sympy import factorint
from num_theory import modular_inverse
from rsa import PrivateKey, PublicKey, decrypt, encrypt, generate_keys
import timeit

#%%


def crack_key(ciphertext : int, public_key : PublicKey):
  prime_factors =factorint(public_key.n).keys()
  assert(len(prime_factors) == 2)
  p,q = prime_factors
  lam = lcm(p-1,q-1)
  d = modular_inverse(public_key.e,lam)
  private_key = PrivateKey(public_key.n, d)
  return decrypt(ciphertext,private_key)
#%%
public, private = generate_keys(80) #2048
m = 42069
ciphertext = encrypt(m,public)
# m_new = crack_key(ciphertext,public)
m_new = -1
def timed_crack():
  global m_new
  m_new = crack_key(ciphertext,public)

time =timeit.timeit(timed_crack,number=1)
print(m,ciphertext,m_new, time)
# %%

# %%
