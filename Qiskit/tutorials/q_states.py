#%%
from numpy import sqrt
from qiskit import QuantumCircuit , Aer
from qiskit.visualization import plot_histogram
sim = Aer.get_backend('aer_simulator')
# %%
qc_state = QuantumCircuit(1)
# coefficients of |0> and |1>
initial_state = [1/sqrt(3),sqrt(2/3)] 
qc_state.initialize(initial_state,0)
qc_state.save_statevector()
qc_state.draw(initial_state=True)
result = sim.run(qc_state)  .result()
result.get_statevector()
counts = result.get_counts()
plot_histogram(counts)
# %%
from qiskit_textbook.widgets import gate_demo
gate_demo(gates='pauli+h+p')

# %%
