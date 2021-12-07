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

# %%
from qiskit import QuantumCircuit, Aer
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit_textbook.widgets import scalable_circuit
from numpy import pi
import warnings

# from qclib.utils import plot_current_bloch_state
warnings.filterwarnings("ignore")

# %%


def crot_k(qc, k, c, t):
    qc.cp(2*pi/(2**k), c, t)


def three_qubit_qft():
    qc = QuantumCircuit(3)
    qc.h(2)
    crot_k(qc, k=2, c=1, t=2)
    crot_k(qc, k=3, c=0, t=2)
    qc.h(1)
    crot_k(qc, k=2, c=0, t=1)
    qc.h(0)
    qc.swap(2, 0)
    return qc


# qc = three_qubit_qft()
# qc.draw()
# %%


def qft(qc: QuantumCircuit, n: int):
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

def iqft(qc : QuantumCircuit, n):
  qft_circ = QuantumCircuit(n)
  qft(qft_circ, n)
  iqft_circ = qft_circ.inverse()
  qc = qc.compose(iqft_circ, qubits=qc.qubits[:n])
  return qc

def gen_iqft_circuit( n):
  qft_circ = QuantumCircuit(n)
  qft(qft_circ, n)
  iqft_circ = qft_circ.inverse()
  return iqft_circ
# %%
# Determine the QFT3 of 5
# qc = QuantumCircuit(3)
# qc.x(0)
# qc.x(2)
# plot_current_bloch_state(qc)
# qft(qc, 3)
# plot_current_bloch_state(qc)
# qc.draw()
# qc.barrier()
# qc = iqft(qc,3)
# plot_current_bloch_state(qc)
# %%
# scalable_circuit(qft)