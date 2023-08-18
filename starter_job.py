import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from qiskit import QuantumCircuit, Aer

class QuantumNeutron:
    def __init__(self, mass, position, momentum):
        self.mass = mass
        self.position = position
        self.momentum = momentum

    def apply_uncertainty(self):
        position_uncertainty = np.random.normal(0, 0.1)
        momentum_uncertainty = np.random.normal(0, 0.05)

        self.position += position_uncertainty
        self.momentum += momentum_uncertainty
        
        print(f"Applied Uncertainty: Position {position_uncertainty:.4f}, Momentum {momentum_uncertainty:.4f}")

def apply_evolution_operator(qc, time_step, position_qubit, momentum_qubit):
    qc.rz(time_step, momentum_qubit)
    qc.rz(-time_step, position_qubit)
    qc.cx(momentum_qubit, position_qubit)
    qc.rz(-time_step, position_qubit)
    qc.cx(momentum_qubit, position_qubit)

def update(frame):
    global neutron, qc, simulator
    neutron.position += neutron.momentum * time_step / neutron.mass
    neutron.momentum -= neutron.position * time_step
    
    apply_evolution_operator(qc, time_step, position_qubit=0, momentum_qubit=1)
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
    
    neutron = QuantumNeutron(mass=1.0, position=0.0, momentum=1.0)

    num_steps = 100
    time_step = 0.1
    positions = []
    momenta = []

    fig, ax = plt.subplots()
    line, = ax.plot([], [], label='Position')
    ax.set_xlim(0, num_steps)
    ax.set_ylim(-10, 10)
    ax.set_xlabel('Time Steps')
    ax.set_ylabel('Value')
    ax.set_title('Neutron Trajectory with Quantum-Inspired Uncertainty')
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
