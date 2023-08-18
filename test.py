import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from qiskit import QuantumCircuit, Aer, executes

class QuantumParticle:
    def __init__(self):
        self.state_vector = np.array([1.0, 0.0])  # Initialize in a position state

    def apply_position_operator(self):
        qc = QuantumCircuit(2)
        qc.h(0)  # Apply a Hadamard gate to create a superposition of positions
        qc.cx(0, 1)  # Apply a controlled-X gate to simulate position evolution
        simulator = Aer.get_backend('statevector_simulator')
        result = execute(qc, simulator).result()
        self.state_vector = result.get_statevector(qc)

def update(frame):
    global particle
    particle.apply_position_operator()

    probabilities = np.abs(particle.state_vector) ** 2

    line.set_xdata(range(len(probabilities)))
    line.set_ydata(probabilities)

    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw()

# ... rest of the code remains the same


def main():
    global particle, positions, momenta, time_step, fig, ax, line
    
    particle = QuantumParticle(mass=1.0, position=0.0, momentum=1.0)
    num_steps = 1000
    time_step = 0.01
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

    ani = FuncAnimation(fig, update, frames=num_steps, repeat=False, interval=50)

    plt.show()

    # Display initial attributes
    print("Initial Attributes:")
    print(f"Mass: {particle.mass}")
    print(f"Position: {particle.position}")
    print(f"Momentum: {particle.momentum}")
    
    # Apply uncertainty inspired by quantum mechanics
    particle.apply_uncertainty()
    
    # Display attributes after applying uncertainty
    print("\nAttributes after Applying Uncertainty:")
    print(f"Mass: {particle.mass}")
    print(f"Position: {particle.position}")
    print(f"Momentum: {particle.momentum}")

if __name__ == "__main__":
    main()
