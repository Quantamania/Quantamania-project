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
    qc.h(0)
    energy = mass * c**2 / hbar
    qc.crx(energy, 0, 1)
    qc.measure(1, 0)
    return qc

# Simulate the quantum circuit for mass values every 100 kg up to 1500 kg
mass_values = np.arange(100, 1501, 100)
shots = 1000

for user_mass in mass_values:
    qc = energy_circuit(user_mass)
    backend = Aer.get_backend('qasm_simulator')
    result = execute(qc, backend, shots=shots).result()
    counts = result.get_counts(qc)
    
    # Get the measured energy
    measured_energy = float(list(counts.keys())[0]) * 1000  # Convert to joules
    
    # Calculate the corresponding mass using E=mc^2
    calculated_mass = measured_energy * hbar / (c**2)
    
    # Print the results for each mass
    print(f"Input Mass: {user_mass:.2e} kg")
    print(f"Predicted Energy: {measured_energy:.2e} J")
    print(f"Calculated Mass: {calculated_mass:.2e} kg\n")

# Plot the histogram of the last measurement outcomes
plot_histogram(counts)