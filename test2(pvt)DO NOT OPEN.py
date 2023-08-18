import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class QuantumParticle:
    def __init__(self, mass, position, momentum):
        self.mass = mass
        self.position = position
        self.momentum = momentum
        self.state = np.array([position, momentum])

    def apply_uncertainty(self):
        position_uncertainty = np.random.normal(0, 0.1)
        momentum_uncertainty = np.random.normal(0, 0.05)
        
        self.state += np.array([position_uncertainty, momentum_uncertainty])
        
        if np.random.rand() < abs(self.position) ** 2:
            self.position = np.random.choice([-1, 1]) * np.sqrt(abs(self.position))

def update(frame):
    global particle
    particle.apply_uncertainty()
    
    particle.position += particle.momentum * time_step / particle.mass
    particle.momentum -= particle.position * time_step
    
    positions.append(particle.position)
    momenta.append(particle.momentum)
    
    line.set_xdata(range(len(positions)))
    line.set_ydata(positions)
    
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw()

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
