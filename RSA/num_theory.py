from typing import Tuple
def bezouts(x : int, y : int) -> Tuple[int ,int,int]:
  """
  Extended Euclidean Algorithm
  Solves for the coefficients a,b in
   a*x + b*y = d
  """

  if x > y:
    s_prev,s_curr = 1,0
    t_prev,t_curr = 0,1
  else:
    x, y = y,x
    s_prev,s_curr = 0,1
    t_prev,t_curr = 1,0
  while  y != 0:
    q = x // y
    x, y  = y, x % y, 
    if y == 0:
      break
    s_curr, s_prev = s_prev- q*s_curr, s_curr
    t_curr, t_prev = t_prev- q*t_curr, t_curr

  gcd = x
  a,b, = s_curr, t_curr
  return a,b,gcd

#Euclidean algorithm
def gcd(a : int, b : int) -> int:
  a, b = (a,b) if a > b else (b,a)
  while  b != 0:
    a, b  = b, a % b
  return a

def lcm(a : int, b : int) -> int:
  return int(a*b/(gcd(a,b)))

def modular_inverse(a,n):
  """
  Solves for b in 
  a*b mod n = 1
  Requirement : GCD(a,n) = 1
  """
  b,_,gcd  = bezouts(a,n)
  assert(gcd == 1)
  return b if b > 0 else n+b