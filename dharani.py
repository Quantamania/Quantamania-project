import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from qiskit import QuantumCircuit, Aer, assemble, transpile
from qiskit.quantum_info import Statevector

class QuantumNeutron:
    def __init__(self, mass, position, momentum):
        self.mass = mass
        self.position = position
        self.momentum = momentum

    def apply_uncertainty(self):
        # Create a quantum circuit with two qubits
        qc = QuantumCircuit(2)

        # Apply a Hadamard gate to the first qubit to create superposition
        qc.h(0)
        
        # Entangle the qubits using a controlled-X (CNOT) gate
        qc.cx(0, 1)

        sv = Statevector.from_label('00')
        sv = sv.evolve(qc)
        print(type(sv.data))
        
        # Simulate the quantum circuit
        backend = Aer.get_backend('statevector_simulator')
        compiled_circuit = transpile(qc, backend)
        qobj = assemble(compiled_circuit, shots=1)
        result = backend.run(qobj).result()

        # Get the statevector after entanglement
        statevector = result.get_statevector()

        # Extract the probabilities of |00> and |11> states
        p_00 = statevector[0]
        p_11 = statevector[3]
        
        # Calculate position and momentum uncertainties based on probabilities
        position_uncertainty = p_00 - p_11
        momentum_uncertainty = p_11 - p_00

        self.position += position_uncertainty
        self.momentum += momentum_uncertainty
        
        print(f"Applied Uncertainty: Position {position_uncertainty:.6f}, Momentum {momentum_uncertainty:.6f}")


def update(frame):
    global neutron, qc, simulator
    neutron.position += neutron.momentum * time_step / neutron.mass
    neutron.momentum -= neutron.position * time_step
    
    
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
    
    neutron = QuantumNeutron(mass=1.0, position=0.0, momentum=2.0)

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
    ax.set_title('Neutron (particle) Trajectory with Quantum-Inspired Uncertainty')
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