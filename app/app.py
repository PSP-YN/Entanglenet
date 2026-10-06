import streamlit as st
import sys
import os

# Add parent directory to path so we can import src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.experiments import run_bb84

st.set_page_config(page_title="EntangleNet - BB84 QKD Simulator", layout="wide")

st.title("EntangleNet: Adaptive BB84 Quantum Key Distribution Simulator")
st.markdown("""
**WARNING**: This is a research/educational simulator, not a production QKD security implementation.
""")

st.sidebar.header("Simulation Parameters")
num_bits = st.sidebar.slider("Number of qubits", min_value=10, max_value=1000, value=100, step=10)
eve_prob = st.sidebar.slider("Eve interception probability (%)", min_value=0, max_value=100, value=0, step=5) / 100.0
noise_prob = st.sidebar.slider("Channel noise (%)", min_value=0, max_value=100, value=0, step=1) / 100.0
seed = st.sidebar.number_input("Random seed", min_value=0, max_value=9999, value=42)

if st.sidebar.button("RUN SIMULATION"):
    with st.spinner("Running BB84 Simulation..."):
        results = run_bb84(num_bits, eve_prob, noise_prob, seed)
        
    st.header("Simulation Results")
    
    col1, col2, col3 = st.columns(3)
    
    col1.metric("Raw Key Length", results['raw_key_length'])
    col2.metric("Sifted Key Length", results['sifted_key_length'])
    col3.metric("Final Key Length", results['estimated_final_key_length'])
    
    col4, col5, col6 = st.columns(3)
    col4.metric("QBER", f"{results['qber']:.2%}")
    col5.metric("Eve Probability", f"{eve_prob:.0%}")
    col6.metric("Noise Probability", f"{noise_prob:.0%}")
    
    st.subheader("Security Status")
    status = results['security_status']
    if "SECURE" in status:
        st.success(status)
    elif "SUSPICIOUS" in status:
        st.warning(status)
    else:
        st.error(status)
        
    st.subheader("Security Explanation")
    st.markdown("""
    **Classical vs PQC vs QKD**:
    - **Classical**: Security based on computational assumptions.
    - **Post-Quantum Cryptography (PQC)**: Classical algorithms designed to resist known quantum attacks.
    - **BB84 QKD**: Security mechanism based on quantum-state disturbance. Note that QKD and PQC are complementary!
    """)
    
    st.subheader("Example Quantum Circuit")
    if results['example_circuit']:
        st.text(results['example_circuit'].draw(output='text'))
        
    st.subheader("Raw Data Preview")
    st.write("Alice Bits:", results['alice_bits'][:20], "...")
    st.write("Alice Bases:", results['alice_bases'][:20], "...")
    st.write("Bob Bases:", results['bob_bases'][:20], "...")
