import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram

# Define constants
c = 3e8  # Speed of light (m/s)
hbar = 1.0545718e-34  # Reduced Planck constant (Joule second)

# Define the quantum circuit
def energy_circuit(mass):
    qc = QuantumCircuit(2, 1)  # Two qubits, one classical bit
    
    # Apply Hadamard gate to create superposition on the first qubit
    qc.h(0)
    
    # Calculate energy using E=mc^2 approximation in a quantum context
    energy = (mass * c**2) / hbar
    
    # Apply a controlled rotation gate between the qubits
    qc.crx(2 * energy, 0, 1)
    
    # Measure the second qubit
    qc.measure(1, 0)
    
    return qc

# Simulate the quantum circuit for different mass values
mass_values = np.linspace(1e-30, 1e-26, 20)  # Range of mass values (kg)
shots = 1000

results = []

for mass in mass_values:
    qc = energy_circuit(mass)
    backend = Aer.get_backend('qasm_simulator')
    job = execute(qc, backend, shots=shots)
    result = job.result()
    counts = result.get_counts(qc)
    results.append(counts)

# Plot the measurement outcomes
energies = [list(counts.keys())[0] for counts in results]
plt.figure(figsize=(10, 6))
plt.plot(mass_values, energies, marker='o')
plt.xlabel("Mass (kg)")
plt.ylabel("Energy (a.u.)")
plt.title("Energy-Mass Relationship")
plt.grid()
plt.show()