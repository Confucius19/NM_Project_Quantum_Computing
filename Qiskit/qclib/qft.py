from qiskit import QuantumCircuit
from numpy import pi

# QFT Building Blocks

# Controlled Phase Rotation (CROT) Gate
# 1 target qubit, 1 control qubit
# CP(θ)
# accessed by qc.cp(<θ>, <control-qubit>, <target-qubit>)
# ╔══════╦═══╦═══╦══════════════╗
# ║ 1    ║ 0 ║ 0 ║ 0            ║
# ╠══════╬═══╬═══╬══════════════╣
# ║      ║ 1 ║ 0 ║ 0            ║
# ║ 0    ║   ║   ║              ║
# ╠══════╬═══╬═══╬══════════════╣
# ║      ║ 0 ║ 1 ║ 0            ║
# ║ 0    ║   ║   ║              ║
# ╠══════╬═══╬═══╬══════════════╣
# ║      ║ 0 ║ 0 ║ exp(i*θ)     ║
# ║ 0    ║   ║   ║              ║
# ╚══════╩═══╩═══╩══════════════╝


# Hadamard Gate
# 1 input
#  accessed by qc.h(<target-qubit>)
#     ╔═══╦════╗
#  1  ║ 1 ║ 1  ║
#  -  ╠═══╬════╣
#  √2 ║ 1 ║ -1 ║
#     ╚═══╩════╝


def crot_k(qc : QuantumCircuit, k, c, t):
    qc.cp(2*pi/(2**k), c, t)


# qc = three_qubit_qft()
# qc.draw()
# %%


def qft(n: int):
  """
  Quantum Fourier Transform in n qubits
  0th index is LSB

  Result in 0th index will be rotation about z 
  axis with phase 2*pi* input/2^n 
  MSB Index point towards |+> if even |-> if odd
  """
  qc =  QuantumCircuit(n)
  # rotate
  for qubit_index in range(n-1, -1, -1):
      qc.h(qubit_index)
      for dependent_qubit_index in range(0, qubit_index):
          crot_k(qc, k=(qubit_index-dependent_qubit_index+1),
                  c=dependent_qubit_index, t=qubit_index)
  # swap
  for qubit_index_1 in range(n//2):
    qubit_index_2 = n-1-qubit_index_1
    qc.swap(qubit_index_1,qubit_index_2)
  return qc

def iqft(n):
  """
  Inverse Quantum Fourier Transform in n qubits
  """
  return qft(n).inverse()