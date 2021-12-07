
#%%
from operator import mod
from typing import Iterable
from matplotlib.pyplot import plot
from qiskit import QuantumCircuit, Aer
from qiskit.compiler.assembler import assemble
from qiskit.compiler.transpiler import transpile
from qiskit.visualization import plot_histogram
from qclib.utils import get_binary_number_representation, not_qubits_from_num, plot_current_bloch_state, statevector_to_binary, not_qubits_from_num
from qiskit.extensions.simulator import snapshot
import pandas as pd
# from qclib import iqft, qft, crot_k
# from qclib.utils import plot_current_bloch_state
# following along with Vedral
# https://arxiv.org/pdf/quant-ph/9511018.pdf


def get_snapshot(result, snapshot_name):
  return result.data()['snapshots']['statevector'][snapshot_name][0]
#%%
def carry_block():
  """
  INDEX:  0,1,2,3
  IN   :  a,b,c,0
  OUT  :  a,b, b XOR c, carry out 
  """
  qc = QuantumCircuit(4)
  qc.ccx(1,2,3)
  qc.cx(1,2)
  qc.ccx(0,2,3)
  qc.name = "Carry"
  return qc


def carry_inverse_block():
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
  qc.name = " Sum "
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

  # main.barrier()
  main.cnot(a_indices[word_size-1], b_indices[word_size-1])
  # main.barrier()
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


  
  main.name = " ADDER "
  return main

def n_bit_adder_inverse(word_size: int):
  return n_bit_adder(word_size).inverse()


# ## add 2 + 3
# qc = QuantumCircuit(10, 4)
# a = 3
# b = 2
# not_qubits_from_num(qc, a,range(3))
# not_qubits_from_num(qc, b,range(3, 6))

# qc.compose(n_bit_adder(3), qubits=range(10), inplace=True)
# qc.barrier()
# qc.measure( range(3, 7), range(4))
# display(qc.draw())
# simulator = Aer.get_backend('aer_simulator')
# results = simulator.run(qc).result()
# counts = results.get_counts()
# plot_histogram(counts)
# qc.draw()

#%%
#https://quantumcomputing.stackexchange.com/questions/6842/is-there-a-simple-formulaic-way-to-construct-a-modular-exponentiation-circuit?noredirect=1&lq=1

def n_bit_modular_adder(word_size: int, modulus : int):
  """
  must pre initialize the modulus in the modulus register
  """
  assert(modulus < 2**word_size)

  a_start = 0
  a_size = word_size
  b_start = a_size
  b_size = word_size + 1
  aux_start = b_start + b_size
  aux_size = word_size
  modulus_start = aux_start + aux_size
  modulus_size = word_size
  tracker_start = modulus_start + modulus_size
  tracker_size = 1
  total_qubits = tracker_start + tracker_size
  a_indices = list(range(a_start, b_start))
  b_indices = list(range(b_start, aux_start))
  aux_indices = list(range(aux_start, modulus_start))
  modulus_indices = list(range(modulus_start,tracker_start ))
  tracker_index = tracker_start

  main = QuantumCircuit(total_qubits)
  # main.snapshot("Init")

  adder_indices = [*a_indices, *b_indices, *aux_indices]
  #BLOCK 1
  #Compute A + B
  main.append(n_bit_adder(word_size), qargs=adder_indices )
  # main.snapshot('PostAdd')
  

  # Compute A + B - N
    ## swap A and N
  def swapAandN():
    for a_index, modulus_index in zip(a_indices, modulus_indices):
      main.swap(a_index, modulus_index)
  swapAandN()

    ## "Subtract" N
  main.append(n_bit_adder_inverse(word_size), qargs=adder_indices )

 

  # Add N back if necessary 
  ## Check Tracker Sign
  ## Carry exists we need to add back and set tracker to 0
  main.x(b_indices[-1])
  main.cnot(b_indices[-1], tracker_index)
  main.x(b_indices[-1])

  # main.snapshot('PostSub')



  ## Transform N -> 0 if necessary
  ###modulus represents as 0th index LSB '01' would be 2
  def conditional_clear_modulus():
    modulus_as_bits = bin(modulus)[2:].zfill(word_size)[::-1]
    for i in range(word_size):
      should_cnot = modulus_as_bits[i] == '1'
      if should_cnot:
        main.cnot(tracker_index, a_indices[i] )

  conditional_clear_modulus()
  # main.snapshot('FirstClear')
  main.append(n_bit_adder(word_size), qargs=adder_indices)
  # main.snapshot('AddBack')
  conditional_clear_modulus()
  # main.snapshot('SecondClear')

  main.barrier()
  swapAandN()
  #Block 2 : Uncompute tracker bit
  main.append(n_bit_adder_inverse(word_size),qargs=adder_indices)
  main.cnot(b_indices[-1],tracker_index)
  main.append(n_bit_adder(word_size),qargs=adder_indices)

  main.name = f"ADD % {modulus}"
  return main

#Modular Adder Circuit Viz
# qc = three_bit_modular_adder(3)
# qc.draw()


#Modular Adder test
## add 2 + 3

# a, b,modulus= 9,13, 17
# word_size = 5
# t_mod_add = n_bit_modular_adder(word_size,modulus)
# qc = QuantumCircuit(t_mod_add.num_qubits, word_size)
# not_qubits_from_num(qc, a, range(word_size))
# not_qubits_from_num(qc, b, range(word_size,2*word_size))
# not_qubits_from_num(qc, a, range(3*word_size+1,4*word_size+1)) #untested modulus range
# qc.append(t_mod_add, qargs=range(t_mod_add.num_qubits))

# qc.measure( range(word_size, 2*word_size), range(word_size))  # a+b mod N
# # display(qc.draw())
# simulator = Aer.get_backend('aer_simulator')
# test =  transpile(qc, simulator)
# result = simulator.run(test).result()
# counts = result.get_counts()
# plot_histogram(counts)

# def svb(statevector,start =0 ,stop=-1, *args, **kwargs):
#   import numpy as np
#   indices = np.where(statevector == 1)
#   assert(len(indices) == 1)
#   num =  indices[0][0]
#   # convert to binary -> truncate 0b -> reverse to qubit order 
#   # -> slice start,stop -> reverse to num order -> cast to int
#   # print(num, bin(num))
#   # print(bin(num)[2:][::-1][start:])#[::-1])
#   # print(start,stop)
#   num = int(bin(num)[2:][::-1][start:stop][::-1].zfill(1),base=2)
#   return num

# snap_names  = ["Init", "PostAdd", "PostSub",
# "FirstClear","AddBack","SecondClear","Final"]
# df =pd.DataFrame(columns=["Name","A", "B", "Aux","N", "t"])

# for snap_name in snap_names:
#   snap = get_snapshot(result, snap_name)
#   df.loc[len(df.index)] = [
#     snap_name,
#     svb(snap,0,3),
#     svb(snap,3,7),
#     svb(snap,7,10),
#     svb(snap,10,13),
#     svb(snap,13,14)
#   ]
# display(df)
#%%
# https://quantumcomputing.stackexchange.com/questions/6842/is-there-a-simple-formulaic-way-to-construct-a-modular-exponentiation-circuit?noredirect=1&lq=1
def n_bit_controlled_modular_multiplier(word_size : int, modulus : int, multiplier: int):
  """
  control  at 0th index
  operand  at range(1,word_size+1)
  output  at range(2*word_size+1,3*word_size+2)
  """
  assert(modulus < 2**word_size)

  input_qubits = word_size + 1
  not_input_qubits = n_bit_modular_adder(word_size,modulus).num_qubits
  total_qubits = input_qubits + not_input_qubits
  main = QuantumCircuit(total_qubits)

  control_index = 0
  operand_indices = list(range(1,word_size+1))
  mod_adder_indices = list(range(word_size+1, total_qubits))

  a_indices = list(range(word_size+1, 2*word_size+1 ))
  output_indices = list(range(2*word_size+1,3*word_size+2)) #word_size +1 long

  # main.snapshot("Init")
  for operand_bit_index in range(word_size):
    factor = (multiplier * 2**operand_bit_index) % modulus
    should_and_array = [bit_str == '1' for bit_str in bin(factor)[2:][::-1]]
    for target_index, should_and in enumerate(should_and_array):
      if should_and:
        main.ccx(control_index,operand_indices[operand_bit_index], a_indices[target_index])
    # main.snapshot(f"PreAddStep{operand_bit_index}")
    main.append(n_bit_modular_adder(word_size,modulus),qargs=mod_adder_indices)
    for target_index, should_and in enumerate(should_and_array):
      if should_and:
        main.ccx(control_index,operand_indices[operand_bit_index], a_indices[target_index])
    # main.snapshot(f"AddStep{operand_bit_index}")

  # put z in output if c is 0
  main.x(control_index)
  for bit_index in range(word_size):
    main.ccx(control_index,operand_indices[bit_index] ,output_indices[bit_index])
  main.x(control_index)

  return main

# three_bit_controlled_modular_multiplier(5, 3).draw()

# #Test modular multiplier
# a,b, modulus = 11,3,15
# word_size =  4
# mult_circ = n_bit_controlled_modular_multiplier(word_size, modulus, b)
# qc = QuantumCircuit(mult_circ.num_qubits, word_size)
# #control bit
# qc.x(0)
# #first term
# not_qubits_from_num(qc,a,range(1,word_size+1))
# #modulus term
# not_qubits_from_num(qc,modulus,range(4*word_size+2,5*word_size+2))

# qc.append(mult_circ, qargs=range(mult_circ.num_qubits))
# qc.snapshot("Final")
# qc.measure(range(2*word_size+1, 3*word_size+1),range(word_size))
# # display(qc.draw())
# simulator = Aer.get_backend('aer_simulator')
# test =  transpile(qc, simulator)
# result = simulator.run(test).result()
# # counts = result.get_counts()
# # display(plot_histogram(counts))

# snap_names  = ["Init", "PreAddStep0", "AddStep0", "PreAddStep1", "AddStep1", "PreAddStep2", "AddStep2", "Final"]
# df =pd.DataFrame(columns=["Name","c", "Z", "0", "output","0","modulus","t"])
# svb= statevector_to_binary
# for snap_name in snap_names:
#   snap = get_snapshot(result, snap_name)
#   df.loc[len(df.index)] = [
#     snap_name,
#     svb(snap,0,1),
#     svb(snap,1,word_size+1),
#     svb(snap,word_size+1,2*word_size+1),
#     svb(snap,2*word_size+1,3*word_size+1),
#     svb(snap,3*word_size+1,4*word_size+2),
#     svb(snap,4*word_size+2,5*word_size+2),
#     svb(snap,5*word_size+2,5*word_size+3)
#   ]
# display(df)

# display(n_bit_controlled_modular_multiplier(4,5,3).draw())
  # result.data()['snapshots']['statevector']
# %%

