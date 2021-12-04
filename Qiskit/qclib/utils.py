from qiskit import QuantumCircuit, Aer
from qiskit.visualization import plot_bloch_multivector
import warnings
warnings.filterwarnings("ignore")

def plot_current_bloch_state(qc : QuantumCircuit, *args, **kwargs):
  sim = Aer.get_backend("aer_simulator")
  qc_to_plot = qc.copy()
  qc_to_plot.save_statevector()
  statevector = sim.run(qc_to_plot).result().get_statevector()
  fig = plot_bloch_multivector(statevector,*args, **kwargs)
  display(fig)