import datetime

def generate_research_paper(results, eve_prob, noise_prob, num_bits):
    """
    Generates a structured research paper draft based on the simulation results.
    """
    qber = results['qber']
    sifted = results['sifted_key_length']
    final_key = results['estimated_final_key_length']
    status = results['security_status']
    leakage = results['reconciliation_leakage']
    
    date_str = datetime.datetime.now().strftime("%B %d, %Y")
    
    paper = f"""# Analysis of BB84 Quantum Key Distribution Under Intercept-Resend Attacks and Channel Noise
**Date:** {date_str}

## Abstract
Quantum Key Distribution (QKD) offers a fundamentally secure method for cryptographic key exchange, secured by the laws of quantum mechanics. The BB84 protocol leverages the no-cloning theorem and state-disturbance principles. In this study, we simulate the BB84 protocol over an unentangled quantum channel to analyze the effect of eavesdropping and channel noise on the Quantum Bit Error Rate (QBER) and final secret key rate.

## 1. Introduction
The rise of quantum computing poses a severe threat to classical cryptographic systems based on integer factorization and discrete logarithms. Post-Quantum Cryptography (PQC) provides computationally secure alternatives, whereas QKD provides information-theoretic security. This paper empirically evaluates the BB84 protocol's resilience when subjected to an intercept-resend attack parameter of $P_{{eve}} = {eve_prob:.2f}$ and channel depolarization noise of $P_{{noise}} = {noise_prob:.2f}$.

## 2. Methodology
The simulation involves the transmission of $N={num_bits}$ photons encoded with random bases ($Z$ or $X$).
- **State Preparation**: Alice generates a classical bit sequence and encodes it into quantum states using Pauli-X and Hadamard gates.
- **Eavesdropping (Eve)**: Eve intercepts photons with a probability of $P_{{eve}}$. She measures the photon in a random basis and resends her collapsed state to Bob.
- **Measurement and Sifting**: Bob measures the photons in random bases. Alice and Bob publicly share their basis choices and discard mismatched bases.
- **Error Correction and Privacy Amplification**: A theoretical perfect error correction algorithm with an efficiency factor $f=1.2$ is modeled. Toeplitz hashing is used for privacy amplification to eliminate Eve's partial information.

## 3. Results
The experiment simulated the transmission of {num_bits} qubits.
After basis reconciliation, the sifted key length was {sifted} bits.

The presence of channel noise and eavesdropping induced a Quantum Bit Error Rate (QBER) of **{qber:.2%}**. 
During the error correction phase, an estimated {leakage} bits of information were theoretically leaked to the public channel. 

Following privacy amplification (which mathematically squeezes out the estimated information gained by Eve bounding her knowledge to 0), the final secure key length was calculated to be **{final_key} bits**.

### 3.1 Security Threshold Analysis
Standard BB84 security proofs assert that for QBER $\ge 11\%$, the channel is compromised and the key must be aborted. 
In our experiment, the recorded QBER ({qber:.2%}) led the system to classify the channel state as: **{status}**.

## 4. Discussion
The empirical results demonstrate the fundamental sensitivity of quantum states to measurement. The intercept-resend attack invariably introduces a disturbance (QBER) proportional to Eve's interception probability. 
When $P_{{eve}} = {eve_prob:.2f}$, the disturbance is clearly observable. If the status is SECURE, the privacy amplification successfully decoupled Eve's correlations. If COMPROMISED, Eve's mutual information with Alice exceeded Bob's, making secure key extraction impossible.

## 5. Conclusion
This study validates the information-theoretic security foundations of BB84. Unlike classical systems where eavesdropping is undetectable, quantum channels fundamentally resist passive surveillance. Future work could integrate decoy states to counter photon-number splitting (PNS) attacks and benchmark against physical hardware noise profiles.

---
*Generated automatically by EntangleNet Simulator*
"""
    return paper
