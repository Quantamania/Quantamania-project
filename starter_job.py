import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from qiskit import QuantumCircuit, Aer, transpile, assemble
from qiskit.visualization import plot_bloch_multivector

class QuantumParticle:
    def __init__(self, mass, position, momentum):
        self.mass = mass
        self.position = position
        self.momentum = momentum

def apply_evolution_operator(qc, time_step, position_qubit, momentum_qubit):
    qc.rz(time_step, momentum_qubit)
    qc.rz(-time_step, position_qubit)
    qc.cx(momentum_qubit, position_qubit)
    qc.rz(-time_step, position_qubit)
    qc.cx(momentum_qubit, position_qubit)

def update(frame):
    global particle, qc, simulator
    particle.position += particle.momentum * time_step / particle.mass
    particle.momentum -= particle.position * time_step
    
    apply_evolution_operator(qc, time_step, position_qubit=0, momentum_qubit=1)
    qc.measure_all()
    
    result = simulator.run(qc).result()
    counts = result.get_counts()
    
    positions.append(particle.position)
    momenta.append(particle.momentum)
    
    line.set_xdata(range(len(positions)))
    line.set_ydata(positions)
    
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw()

def main():
    global particle, positions, momenta, time_step, fig, ax, line, qc, simulator
    
    particle = QuantumParticle(mass=1.0, position=0.0, momentum=1.0)
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
    ax.set_title('Particle Trajectory with Quantum-Inspired Uncertainty')
    ax.legend()

    simulator = Aer.get_backend('qasm_simulator')
    qc = QuantumCircuit(2)

    ani = FuncAnimation(fig, update, frames=num_steps, repeat=False, interval=500)

    plt.show()

    # Display initial attributes
    print("Initial Attributes:")
    print(f"Mass: {particle.mass}")
    print(f"Position: {particle.position}")
    print(f"Momentum: {particle.momentum}")

if __name__ == "__main__":
    main()
