import streamlit as st
import sys
import os

# Add parent directory to path so we can import src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.experiments import run_bb84

st.set_page_config(page_title="EntangleNet - QKD Simulator", layout="wide", page_icon="⚛️")

# Custom CSS for aesthetics
st.markdown("""
<style>
.metric-box {
    background-color: #1e1e2e;
    border-radius: 10px;
    padding: 20px;
    margin: 10px 0;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}
.title-text {
    font-size: 3.5rem;
    font-weight: 800;
    background: -webkit-linear-gradient(45deg, #FF6B6B, #4ECDC4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding-bottom: 10px;
}
div[data-testid="metric-container"] {
    background-color: #1a1a24;
    border: 1px solid #333;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title-text">EntangleNet: Adaptive BB84 Simulator</p>', unsafe_allow_html=True)
st.markdown("""
Welcome to **EntangleNet**. This simulator demonstrates the information-theoretic security of the BB84 Quantum Key Distribution protocol. 
Adjust the parameters on the sidebar to simulate eavesdropping and quantum channel noise, and see how the No-Cloning theorem fundamentally protects the key.
""")

st.sidebar.header("🔬 Simulation Parameters")
num_bits = st.sidebar.slider("Number of qubits", min_value=100, max_value=2000, value=500, step=100)
eve_prob = st.sidebar.slider("Eve interception probability (%)", min_value=0, max_value=100, value=0, step=5) / 100.0
noise_prob = st.sidebar.slider("Channel noise (%)", min_value=0, max_value=100, value=0, step=1) / 100.0
seed = st.sidebar.number_input("Random seed (0 for random)", min_value=0, max_value=9999, value=0)

st.sidebar.markdown("---")
if st.sidebar.button("🚀 RUN SIMULATION", type="primary", use_container_width=True):
    with st.spinner("Preparing quantum states & executing measurements via Qiskit..."):
        # Use None if seed is 0 to allow true randomness
        actual_seed = seed if seed != 0 else None
        results = run_bb84(num_bits, eve_prob, noise_prob, actual_seed)
        st.session_state['results'] = results
        st.session_state['eve_prob'] = eve_prob
        st.session_state['noise_prob'] = noise_prob
        st.session_state['num_bits'] = num_bits

if 'results' in st.session_state:
    results = st.session_state['results']
    st.divider()
    st.header("📊 Simulation Results")
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Raw Key Length", results['raw_key_length'], "Qubits Transmitted")
    with col2:
        st.metric("Sifted Key", results['sifted_key_length'], "After Reconciliation")
    with col3:
        st.metric("Final Key", results['estimated_final_key_length'], "Post Privacy Amp")
    with col4:
        # Show delta as inverse so high QBER is red
        delta_val = f"{results['qber']:.2%}" if results['qber'] > 0 else None
        st.metric("QBER (Error Rate)", f"{results['qber']:.2%}", delta_val, delta_color="inverse")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.subheader("🛡️ Security Status")
    status = results['security_status']
    if "SECURE" in status:
        st.success(f"**{status}**: The QBER is within safe limits. Eve's information has been squeezed out.")
    elif "SUSPICIOUS" in status:
        st.warning(f"**{status}**: Elevated QBER detected. Proceed with extreme caution or abort.")
    else:
        st.error(f"**{status}**: Critical QBER threshold exceeded! Eavesdropper or heavy noise detected. Key aborted.")
        
    st.divider()
    
    st.subheader("🔬 Deep Dive: Quantum Level")
    tab1, tab2 = st.tabs(["Raw Data Preview", "Example Quantum Circuit"])
    
    with tab1:
        st.info("This is the raw data showing Alice's random bits, the measurement bases chosen, and Bob's bases. In the BB84 protocol, they only keep the bits where their bases matched.")
        st.code(f"Alice Bits:  {results['alice_bits'][:60]}...\n"
                f"Alice Bases: {results['alice_bases'][:60]}...\n"
                f"Bob Bases:   {results['bob_bases'][:60]}...", language="text")
        
    with tab2:
        if results['example_circuit']:
            st.markdown("Here is how one of the qubits looks when encoded as a quantum circuit before transmission:")
            st.code(results['example_circuit'].draw(output='text'), language="text")
