import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def apply_intercept_resend(circuits: list[QuantumCircuit], eve_probability: float) -> list[QuantumCircuit]:
    """
    Simulates Eve's intercept-resend attack on the quantum channel.
    Eve intercepts a fraction of qubits based on eve_probability,
    measures them in a random basis, and prepares a new qubit to resend.
    """
    if eve_probability == 0.0:
        return circuits
        
    simulator = AerSimulator()
    n = len(circuits)
    intercepted = np.random.rand(n) < eve_probability
    eve_bases = np.random.randint(2, size=n)
    
    final_circuits = []
    measure_circuits = []
    intercept_indices = []
    
    for i, (qc, intercept, basis) in enumerate(zip(circuits, intercepted, eve_bases)):
        if intercept:
            measure_qc = qc.copy()
            if basis == 1:
                measure_qc.h(0)
            measure_qc.measure_all()
            measure_circuits.append(measure_qc)
            intercept_indices.append(i)
            
    if measure_circuits:
        job = simulator.run(measure_circuits, shots=1)
        result = job.result()
        
        eve_results = []
        for i in range(len(measure_circuits)):
            counts = result.get_counts(i)
            eve_results.append(int(list(counts.keys())[0]))
            
    # Reconstruct the sequence of circuits sent to Bob
    eve_idx = 0
    for intercept, basis in zip(intercepted, eve_bases):
        if intercept:
            # Eve resends what she measured
            resend_qc = QuantumCircuit(1)
            bit = eve_results[eve_idx]
            if bit == 1:
                resend_qc.x(0)
            if basis == 1:
                resend_qc.h(0)
            final_circuits.append(resend_qc)
            eve_idx += 1
        else:
            # Not intercepted, we need the original circuit. 
            # We will grab it by index below.
            pass
            
    # Actually need to iterate properly to keep the original ones intact
    final_circuits = []
    eve_idx = 0
    for qc, intercept, basis in zip(circuits, intercepted, eve_bases):
        if intercept:
            resend_qc = QuantumCircuit(1)
            bit = eve_results[eve_idx]
            if bit == 1:
                resend_qc.x(0)
            if basis == 1:
                resend_qc.h(0)
            final_circuits.append(resend_qc)
            eve_idx += 1
        else:
            final_circuits.append(qc.copy())
            
    return final_circuits
