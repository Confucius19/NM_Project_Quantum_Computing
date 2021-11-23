
def carmichael_totient(n, is_prime=True):
  #computes the number of coprime numbers less than n

  # is_coprime(a,b) := gcd(a,b) == 1
  # primes are coprime with every lesser number
  if is_prime:
    return n - 1
  else:
    raise NotImplementedError()