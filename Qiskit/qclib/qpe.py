from qiskit import QuantumCircuit
from .qft import iqft


def qpe(t : int, psi : QuantumCircuit, U) -> int: 
  """
  Quantum Phase Esimation

  t : num counting qubits
  psi : quantum circuit in eigenstate (with proper number of qubits)
  U(a: int) : Returns quantum circuit that represent unitary operator to power a
  """
  #put counting bits into 0 degree phase (superposition)
  main_circuit = QuantumCircuit(t+psi.num_qubits, t)

  eigenstate_qubit_indices = list(range(t,t+psi.num_qubits))
  main_circuit.compose(psi,qubits=eigenstate_qubit_indices, inplace=True)


  for i in range(t):
    main_circuit.h(i)
  

  main_circuit.barrier() 
  #Apply Controlled Unitary Operations
  for i in range(t):
    op = U(2**i)
    main_circuit.compose(op,qubits=[i,*eigenstate_qubit_indices ], inplace=True)


  main_circuit.barrier() 
  #Inverse QFT
  iqft_circuit = iqft(t)
  main_circuit.compose(iqft_circuit,qubits=list(range(t)), inplace=True)

  main_circuit.barrier() 
  # Measure Counting Bits
  main_circuit.measure(list(range(t)), list(range(t)))

  return main_circuit