import os
from dotenv import load_dotenv

load_dotenv()

IBM_RESOURCE= os.getenv('IBM_RESOURCE')


import strangeworks as sw
import qiskit
from strangeworks_qiskit import StrangeworksProvider

# get your API key from the Strangeworks Portal
sw.authenticate(
    api_key=IBM_RESOURCE,
)

client =sw.Client()

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

# Choose a backend (the IBM-hosted simulator in this case)
backend = provider.get_backend("ibmq_qasm_simulator")

# Execute the circuit
print('\n🤖 Executing Circuit...\n')


import strangeworks as sw


# Submit the job to Strangeworks
job = client.submit_job(
    script="starter_job.py",
    runtime="qiskit",
)

job.wait()
# At this point, the job is running on the Strangeworks Platform.
# You can check the status of the job in the Portal, even if 
# stop this script.
print(f'⏳ Job {job._job_slug} submitted!\n')

# Lots of good info in here
result = job.result()

# View the counts (also visible in the Portal in a chart 📊) 
counts = result.get_counts()
print(f"🎉 📊 Counts: {counts}\n")
