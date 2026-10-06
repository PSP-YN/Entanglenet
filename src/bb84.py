import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def generate_bits(n: int) -> np.ndarray:
    """Generates n random classical bits."""
    return np.random.randint(2, size=n)

def generate_bases(n: int) -> np.ndarray:
    """Generates n random bases. 0 corresponds to Z basis, 1 corresponds to X basis."""
    return np.random.randint(2, size=n)

def encode_bits_to_quantum_circuits(bits: np.ndarray, bases: np.ndarray) -> list[QuantumCircuit]:
    """
    Encodes bits into quantum states based on the selected bases.
    Z basis (0): bit 0 -> |0>, bit 1 -> |1>
    X basis (1): bit 0 -> |+>, bit 1 -> |->
    """
    circuits = []
    for bit, basis in zip(bits, bases):
        qc = QuantumCircuit(1)
        if bit == 1:
            qc.x(0)
        if basis == 1:
            qc.h(0)
        circuits.append(qc)
    return circuits

def measure_quantum_states(circuits: list[QuantumCircuit], bob_bases: np.ndarray, noise_model=None) -> np.ndarray:
    """
    Measures quantum states using Bob's selected bases.
    """
    simulator = AerSimulator(noise_model=noise_model) if noise_model else AerSimulator()
    measured_circuits = []
    
    for qc, basis in zip(circuits, bob_bases):
        measure_qc = qc.copy()
        if basis == 1:
            measure_qc.h(0)
        measure_qc.measure_all()
        measured_circuits.append(measure_qc)
        
    job = simulator.run(measured_circuits, shots=1)
    results = job.result()
    
    measured_bits = []
    for i in range(len(circuits)):
        counts = results.get_counts(i)
        measured_bit = int(list(counts.keys())[0])
        measured_bits.append(measured_bit)
        
    return np.array(measured_bits)
