import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from qiskit import QuantumCircuit, Aer

class QuantumNeutron:
    def __init__(self, mass, position, momentum):
        self.mass = mass
        self.position = position
        self.momentum = momentum

def apply_entanglement(qc, position_qubit, momentum_qubit):
    qc.h(position_qubit)
    qc.cx(position_qubit, momentum_qubit)
    qc.cx(momentum_qubit, position_qubit)
    qc.h(momentum_qubit)

def apply_evolution_operator(qc, time_step, position_qubit, momentum_qubit):
    """
    Apply the quantum evolution operator for the neutron.

    Args:
        qc: The quantum circuit.
        time_step: The time step.
        position_qubit: The qubit representing the position of the neutron.
        momentum_qubit: The qubit representing the momentum of the neutron.
    """

    qc.rz(time_step * neutron.mass, position_qubit)
    qc.rx(time_step * neutron.momentum, momentum_qubit)
    qc.cx(position_qubit, momentum_qubit)


def update(frame):
    global neutron, qc, simulator
    neutron.position += neutron.momentum * time_step / neutron.mass
    neutron.momentum -= neutron.position * time_step
    
    apply_evolution_operator(qc, time_step, position_qubit=0, momentum_qubit=1)
    apply_entanglement(qc, position_qubit=0, momentum_qubit=1)
    qc.measure_all()
    
    result = simulator.run(qc).result()
    counts = result.get_counts()
    
    neutron.position = (neutron.position + neutron.momentum) / 2
    neutron.momentum = (neutron.momentum - neutron.position) / 2
    
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
    ax.set_title('Neutron Trajectory with Entanglement')
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
