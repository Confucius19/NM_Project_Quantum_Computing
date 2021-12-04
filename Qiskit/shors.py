#%%
from qiskit.visualization.counts_visualization import plot_histogram
from tutorials.qpe import qpe
from qiskit import Aer, QuantumCircuit
from numpy import pi
import math
# %%

"""
#Conventions
0th index qubit is MSB



qpe needs to know 3 things
1.
 t : int :number of "counting" qubits to use 
  For facotring, shor recomends  n^2< 2^t <2n^2 where n is the size of the integer we are factoring

2.
psi : QuantumCircuit;  the eigenstate of the unitary operator
should be |1>
represented by at least the number of bits required to represent n, the integer
we are factoring

3.
U : func(power)->QuantumCircuit; function that generates a Quantum Circuit that
will apply the controlled unitary operation with 0 as control bit 
"""

#%%
def findNumBitsRequired(n) -> int:
  return math.ceil(2*math.log2(n))

def generate_shor_eigenstate(n):
  """
  0th index qubit is MSB
  Generate the number 1 in n qubits
  """
  qc = QuantumCircuit(n)
  qc.x(n-1) 
  return qc


def shors_unitary_generator(a,N):
  """
  U |y> = |a*y (mod N)>

  2.
  """

  def shors_unitary(a: int):
    """
    """
    pass

  return shors_unitary









# simulator = Aer.get_backend('aer_simulator')


# %%
