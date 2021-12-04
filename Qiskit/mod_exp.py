#%%
from qiskit import QuantumCircuit, Aer
from qiskit.circuit.gate import Gate
from qiskit.visualization import plot_histogram
from qclib import iqft, qft, crot_k
from qclib.utils import plot_current_bloch_state
# following along with Vedral
# https://arxiv.org/pdf/quant-ph/9511018.pdf


#%%
def carry_block() -> Gate:
  """
  INDEX:  0,1,2,3
  IN   :  a,b,c,0
  OUT  :  a,b, b XOR c, carry out 
  """
  qc = QuantumCircuit(4)
  qc.ccx(1,2,3)
  qc.cx(1,2)
  qc.ccx(0,2,3)
  # gate = qc.to_gate(label="Carry")
  # gate.name = " Carry "
  return qc

def carry_inverse_block()->Gate:
 cb = carry_block()
 return cb.inverse()

def sum_block() -> QuantumCircuit:
  """
  INDEX:  0,1,2
  IN   :  a,b,c
  OUT  :  a,b, a XOR b XOR c (sum)
  """
  qc = QuantumCircuit(3)
  qc.cx(1,2)
  qc.cx(0,2)
  # gate = qc.to_gate()
  # gate.name = " Sum "
  return qc

def sum_inverse_block()-> QuantumCircuit:
 sb = sum_block()
 return sb.inverse()


def n_bit_adder(word_size: int):
  """
  0th index LSB
   
  Output at indices range(word_size, 2*word_size+1)
  """
  a_start = 0
  b_start = word_size
  aux_start = b_start + word_size+1
  total_qubits = aux_start + word_size
  a_indices = list(range(a_start, b_start))
  b_indices = list(range(b_start, aux_start))
  aux_indices = list(range(aux_start, total_qubits))
  main = QuantumCircuit(total_qubits)
  for i in range(word_size):
    cb = carry_block()
    aux_LSB_index = aux_indices[i]
    a_index = a_indices[i]
    b_index = b_indices[i]
    aux_MSB_index = b_indices[-1] if i + 1+ aux_start >= total_qubits  else aux_indices[i + 1]
    main.compose(cb,qubits=[aux_LSB_index, a_index, b_index, aux_MSB_index], inplace=True)

  main.barrier()
  main.cnot(a_indices[word_size-1], b_indices[word_size-1])
  main.barrier()
  for i in range(word_size-1,-1,-1):
    aux_LSB_index = aux_indices[i]
    a_index = a_indices[i]
    b_index = b_indices[i]
    aux_MSB_index = b_indices[-1] if i + 1+ aux_start >= total_qubits  else aux_indices[i + 1]
    if i != word_size -1:
      # Inverse CARRY
      cb_inverse = carry_inverse_block()
      main.compose(cb_inverse,qubits=[aux_LSB_index, a_index, b_index, aux_MSB_index], inplace=True)

    sb = sum_block()
    main.compose(sb,qubits=[aux_LSB_index, a_index, b_index], inplace=True)


  
  return main


#%%
## add 2 + 3
qc = QuantumCircuit(10, 4)
# a= 1
qc.x(0)
qc.x(1)
qc.x(2)

# b= 3
qc.x(3)
qc.x(4)
qc.x(5)


qc.compose(n_bit_adder(3), qubits=range(10), inplace=True)
qc.barrier()
qc.measure( range(3, 7), range(4))
# qc.draw()
simulator = Aer.get_backend('aer_simulator')
results = simulator.run(qc).result()
counts = results.get_counts()
plot_histogram(counts)
# qc.draw()



# #%%
# qc = QuantumCircuit(3)
# qc.append(sum_inverse_block(), qargs=range(3))
# qc.draw()
# qc = QuantumCircuit(4)
# qc.append(carry_inverse_block(), qargs=range(4))
# qc.draw()


# # #%%

# # def plain_adder(operand_num_qubits: int) -> QuantumCircuit:
# #   """
# #   |a,b>  -> |a, a+b mod 2^n> (qft style)

# #   A input: indices -> 0:operand_num_qubits-1 (size: operand_num_qubits)
# #   B input: indices -> operand_num_qubits:2*operand_num_qubits (size:
# #   operand_num_qubits)
# #   """

# #   qc = QuantumCircuit(2*(operand_num_qubits+1))
# #   a_indices = list(range(operand_num_qubits+1)) 
# #   b_indices = list(range(operand_num_qubits+1, 2*operand_num_qubits+2)) 
# #   qc.compose(qft(len(b_indices)),qubits=b_indices, inplace=True) 
# #   qc.barrier()
# #   plot_current_bloch_state(qc, title="pre rot")

# #   qc.barrier()
# #   for index, b_index in enumerate(b_indices):
# #     for index in range(operand_num_qubits+1-index):
# #       crot_k(qc,index+1, a_indices[index], b_index)


# #   qc.barrier()
# #   plot_current_bloch_state(qc, title="post rot")

# #   qc.compose(iqft(len(b_indices)),qubits=b_indices, inplace=True) 

# #   return qc


# # #%%

# # from qiskit import Aer
# # from qiskit.visualization import plot_histogram


# # qc_test = QuantumCircuit(4)
# # # a = 2
# # qc_test.x(1)
# # # c = 2
# # qc_test.x(3)
# # plot_current_bloch_state(qc_test, title="Initial State")
# # qc_test.compose(plain_adder(3),qubits=range(4), inplace=True)
# # plot_current_bloch_state(qc_test, title="Before Measurement")
# # qc_test.measure_all()

# # simulator = Aer.get_backend('aer_simulator')
# # results = simulator.run(qc_test).result()
# # counts = results.get_counts()
# # display(qc_test.draw())
# # plot_histogram(counts)


# # # %%

# # # %%

# # # def adder_qft(operand_num_qubits: int):
# # #   """
# # #   A input: indices -> 0:operand_num_qubits-1 (size: operand_num_qubits)
# # #   B input: indices -> operand_num_qubits:2*operand_num_qubits (size:
# # #   operand_num_qubits + 1)
  
# # #   """
# # #   qc = QuantumCircuit(2*operand_num_qubits+1)
# # #   b_indices = list(range(operand_num_qubits, 2*operand_num_qubits+1)) 
# # #   qc.compose(qft(len(b_indices)),qubits=b_indices, inplace=True) 
# # #   qc.barrier()

# # #   a_indices = list(range(operand_num_qubits)) 

# %%
