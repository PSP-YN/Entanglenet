import numpy as np

def sift_key(alice_bits: np.ndarray, alice_bases: np.ndarray, bob_bases: np.ndarray, bob_results: np.ndarray):
    """
    Performs basis reconciliation (sifting).
    Keeps only the bits where Alice and Bob randomly chose the same basis.
    """
    matching_bases = alice_bases == bob_bases
    alice_sifted = alice_bits[matching_bases]
    bob_sifted = bob_results[matching_bases]
    return alice_sifted, bob_sifted
