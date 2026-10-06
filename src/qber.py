import numpy as np

def calculate_qber(alice_sifted: np.ndarray, bob_sifted: np.ndarray):
    """
    Calculates the Quantum Bit Error Rate (QBER).
    QBER = mismatched bits / total compared bits.
    """
    if len(alice_sifted) == 0:
        return 0, 0, 0.0
        
    mismatches = np.sum(alice_sifted != bob_sifted)
    qber = mismatches / len(alice_sifted)
    return len(alice_sifted), mismatches, qber
