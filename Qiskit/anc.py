#%%
from qiskit import QuantumCircuit
from qiskit.circuit.gate import Gate
from qiskit.circuit.quantumregister import AncillaRegister
# %%
def gen_test_gate() -> Gate:
  active_reg = QuantumCircuit(1)
  anc_reg = AncillaRegister(1)
  active_reg.add_register(anc_reg)
  active_reg.x(0)
  gate = active_reg.to_gate()
  return gate


qc = QuantumCircuit(2)
qc.append(gen_test_gate(), qargs=[0,1])
qc.draw()


# %%
