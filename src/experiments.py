from .bb84 import generate_bits, generate_bases, encode_bits_to_quantum_circuits, measure_quantum_states
from .attacks import apply_intercept_resend
from .quantum_channel import get_channel_noise_model
from .sifting import sift_key
from .qber import calculate_qber
from .error_correction import apply_error_correction
from .privacy_amplification import privacy_amplification
from .security import check_security

def run_bb84(num_bits: int, eve_probability: float, noise_probability: float, seed: int = None):
    """
    Runs a full BB84 simulation end-to-end.
    """
    import numpy as np
    if seed is not None:
        np.random.seed(seed)
        
    alice_bits = generate_bits(num_bits)
    alice_bases = generate_bases(num_bits)
    
    circuits = encode_bits_to_quantum_circuits(alice_bits, alice_bases)
    
    intercepted_circuits = apply_intercept_resend(circuits, eve_probability)
    
    noise_model = get_channel_noise_model(noise_probability)
    
    bob_bases = generate_bases(num_bits)
    bob_results = measure_quantum_states(intercepted_circuits, bob_bases, noise_model)
    
    alice_sifted, bob_sifted = sift_key(alice_bits, alice_bases, bob_bases, bob_results)
    
    sifted_len, mismatches, qber = calculate_qber(alice_sifted, bob_sifted)
    
    corrected_key, errors_detected, leakage = apply_error_correction(alice_sifted, bob_sifted)
    
    final_key = privacy_amplification(corrected_key, qber, leakage)
    
    security_status = check_security(qber)
    
    return {
        "raw_key_length": num_bits,
        "sifted_key_length": sifted_len,
        "mismatches": mismatches,
        "qber": qber,
        "errors_detected": errors_detected,
        "reconciliation_leakage": leakage,
        "estimated_final_key_length": len(final_key),
        "final_key": final_key,
        "security_status": security_status,
        "alice_bits": alice_bits,
        "alice_bases": alice_bases,
        "bob_bases": bob_bases,
        "bob_results": bob_results,
        "example_circuit": circuits[0] if circuits else None
    }
