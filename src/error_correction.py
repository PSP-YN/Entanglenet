import numpy as np

def apply_error_correction(alice_sifted: np.ndarray, bob_sifted: np.ndarray):
    """
    An educational, simplified error correction simulation.
    In practice, protocols like Cascade or Winnow are used.
    Here, we assume perfect error correction where Bob magically corrects his bits 
    to match Alice's, but we account for the information leaked during this process.
    """
    if len(alice_sifted) == 0:
        return np.array([]), 0, 0
        
    mismatches = np.sum(alice_sifted != bob_sifted)
    qber = mismatches / len(alice_sifted)
    
    # Simulate perfect correction (Bob's key becomes Alice's)
    corrected_key = alice_sifted.copy()
    
    # Calculate Shannon entropy h(QBER) to estimate leaked bits
    if qber == 0:
        h_qber = 0.0
    elif qber >= 0.5:
        h_qber = 1.0
    else:
        h_qber = -qber * np.log2(qber) - (1 - qber) * np.log2(1 - qber)
        
    # f(QBER) > 1 represents inefficiency of real error correction protocols.
    # We use f = 1.2 as a typical value.
    f = 1.2
    leakage = int(np.ceil(f * h_qber * len(alice_sifted)))
    
    return corrected_key, mismatches, leakage
