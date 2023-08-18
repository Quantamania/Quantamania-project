import os
from dotenv import load_dotenv

load_dotenv()

IBM_RESOURCE= os.getenv('IBM_RESOURCE')


import strangeworks
import qiskit
from strangeworks_qiskit import StrangeworksProvider

# get your API key from the Strangeworks Portal
strangeworks.authenticate(
    api_key=IBM_RESOURCE,
)

# Optional: If you have multiple instances (resources) of a product, 
# you can set the resource to use here.
# strangeworks.set_resource_for_product('your-resource-slug', 'ibm-quantum')

# This is your replacement Qiskit Provider that allows you to use
# the Strangeworks Platform as a backend for Qiskit.
provider = StrangeworksProvider()

# Optional: You can list the Qiskit-compatible backends available on 
# the Strangeworks Platform
backends = provider.backends()
print('Available backends:')
for backend in backends:
    print(f'  - {backend.name()}')

# create a simple quantum circuit
qc = qiskit.QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

# Choose a backend (the IBM-hosted simulator in this case)
backend = provider.get_backend("ibmq_qasm_simulator")

# Execute the circuit
print('\n🤖 Executing Circuit...\n')

job = qiskit.execute(qc, backend, shots=100)

# At this point, the job is running on the Strangeworks Platform.
# You can check the status of the job in the Portal, even if 
# stop this script.
print(f'⏳ Job {job._job_slug} submitted!\n')

# Lots of good info in here
result = job.result()

# View the counts (also visible in the Portal in a chart 📊) 
counts = result.get_counts()
print(f"🎉 📊 Counts: {counts}\n")
