import tkinter
import tkinter.messagebox
import customtkinter

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from qiskit import QuantumCircuit, Aer, transpile, assemble
import random

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

mass=1.008
position=0.0
momentum=0.01

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

    neutron = QuantumNeutron(mass,position,momentum)

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

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Quantum Particle Simulator", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Start Simulation" , command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.particle_choice = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Neutron", "Electron"],
                                                                       command=self.change_appearance_mode_event)
        self.particle_choice.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Enter the Constants")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", text="Update Momentum", border_width=2, text_color=("gray10", "#DCE4EE"),command=self.change_defaults_mom)
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.entry2 = customtkinter.CTkEntry(self, placeholder_text="Enter the Constants")
        self.entry2.grid(row=4, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_2 = customtkinter.CTkButton(master=self, fg_color="transparent", text="Update Position", border_width=2, text_color=("gray10", "#DCE4EE"),command=self.change_defaults_pos)
        self.main_button_2.grid(row=4, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")


        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

        self.Text_box = "Current Constants\n\n" + "Mass-{0}\n Position={1}\nMomentum={2}\n".format(mass, position, momentum)

        self.textbox.insert("0.0",self.Text_box)

    
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def change_defaults_mom(self):
        print("func called")
        momentum = self.entry.get()
        print(momentum)
        self.Text_box = "Current Constants\n\n" + "Mass-{0}\n Position={1}\nMomentum={2}\n\n\n--------------------".format(mass, position, self.entry.get())
        self.textbox.insert("0.0",self.Text_box)

    def change_defaults_pos(self):
        print("func called")
        position = self.entry2.get()
        print(position)
        self.Text_box = "Current Constants\n\n" + "Mass-{0}\n Position={1}\nMomentum={2}\n\n\n--------------------".format(mass, position, self.entry2.get())
        self.textbox.insert("0.0",self.Text_box)

    def sidebar_button_event(self):
        main()
        print("sidebar_button click")


if __name__ == "__main__":
    app = App()
    app.mainloop()
    