import numpy as np

def privacy_amplification(corrected_key: np.ndarray, qber: float, leakage: int) -> np.ndarray:
    """
    Applies privacy amplification to reduce Eve's potential information.
    We use a simplified Toeplitz-hashing approach by multiplying the key 
    by a random binary matrix.
    """
    if len(corrected_key) == 0:
        return np.array([])
        
    # Estimate information Eve might have gained. 
    # For intercept-resend, Eve's info in asymptotic limit is bounded by h(QBER).
    if qber == 0:
        h_qber = 0.0
    elif qber >= 0.5:
        h_qber = 1.0
    else:
        h_qber = -qber * np.log2(qber) - (1 - qber) * np.log2(1 - qber)
        
    eve_leakage = int(np.ceil(h_qber * len(corrected_key)))
    
    # Calculate final key length
    final_length = len(corrected_key) - leakage - eve_leakage
    
    if final_length <= 0:
        # Key is fully compromised or too short
        return np.array([])
        
    # Generate random binary matrix for hashing (simplified Toeplitz)
    np.random.seed(42)  # Fixed seed for reproducibility in this educational context
    hash_matrix = np.random.randint(2, size=(final_length, len(corrected_key)))
    
    # Hash the key
    final_key = np.dot(hash_matrix, corrected_key) % 2
    return final_key
