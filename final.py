import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from qiskit import QuantumCircuit, Aer, transpile, assemble
import random

class QuantumNeutron:
    def __init__(self, mass, position, momentum):
        self.mass = mass
        self.position = position
        self.momentum = momentum

    def apply_uncertainty(self):
        random_bits = quantum_random_bit_generator(2)       

        # Convert the random bits to an integer
        random_integer = int(random_bits, 2)

        # Use a classical random number generator to decide the sign
        if random.random() < 0.5:
            random_integer *= -1

        position_uncertainty = np.random.normal(0, 0.1) + random_integer/2
        momentum_uncertainty = np.random.normal(0, 0.05) + random_integer/2

        self.position += position_uncertainty
        self.momentum += momentum_uncertainty


def quantum_random_bit_generator(num_bits):
    # Create a quantum circuit with num_bits qubits
    circuit = QuantumCircuit(num_bits, num_bits)
    
    # Apply Hadamard gates to create superposition
    for i in range(num_bits):
        circuit.h(i)
    
    # Measure the qubits
    circuit.measure(range(num_bits), range(num_bits))
    
    # Simulate the circuit on a quantum simulator
    simulator = Aer.get_backend('qasm_simulator')
    job = assemble(transpile(circuit, simulator), shots=1)
    result = simulator.run(job).result()
    
    # Get the measured classical bits
    random_bits = list(result.get_counts().keys())[0]
    
    return random_bits

    



def apply_entanglement(qc, position_qubit, momentum_qubit):
    qc.h(position_qubit)
    qc.cx(position_qubit, momentum_qubit)
    qc.cx(momentum_qubit, position_qubit)
    qc.h(momentum_qubit)

def apply_evolution_operator(qc, time_step, position_qubit, momentum_qubit, neutron_mass):
    qc.rz(time_step * neutron_mass, position_qubit)
    qc.rx(time_step * neutron_mass, momentum_qubit)
    qc.cx(position_qubit, momentum_qubit)

def update(frame):
    global neutron, qc, simulator
    neutron.position += neutron.momentum * time_step / neutron.mass
    neutron.momentum -= neutron.position * time_step

    apply_evolution_operator(qc, time_step, position_qubit=0, momentum_qubit=1, neutron_mass=neutron.mass)
    apply_entanglement(qc, position_qubit=0, momentum_qubit=1)
    qc.measure_all()

    result = simulator.run(qc).result()
    counts = result.get_counts()

    neutron.apply_uncertainty()  # Apply uncertainty after updating position and momentum

    positions.append(neutron.position)
    momenta.append(neutron.momentum)

    line.set_xdata(range(len(positions)))
    line.set_ydata(positions)

    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw()

def main():
    global neutron, positions, momenta, time_step, fig, ax, line, qc, simulator

    neutron = QuantumNeutron(mass=1.008, position=0.0, momentum=0.01)

    num_steps = 100
    time_step = 0.1
    positions = []
    momenta = []

    fig, ax = plt.subplots()
    line, = ax.plot([], [], label='Position')
    ax.set_xlim(0, num_steps)
    ax.set_ylim(-10, 10)
    ax.set_xlabel('Time Steps')
    ax.set_ylabel('Position')
    ax.set_title('Neutron (Particle) Trajectory with Quantum-Inspired Uncertainty')
    ax.legend()

    simulator = Aer.get_backend('qasm_simulator')
    qc = QuantumCircuit(2)

    ani = FuncAnimation(fig, update, frames=num_steps, repeat=False, interval=500)

    plt.show()

    # Display initial attributes
    print("Initial Attributes:")
    print(f"Position: {neutron.position}")
    print(f"Momentum: {neutron.momentum}")

if __name__ == "__main__":
    main()
