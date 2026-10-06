import streamlit as st
import sys
import os

# Add parent directory to path so we can import src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.experiments import run_bb84
from src.paper_generator import generate_research_paper

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
    font-size: 3rem;
    font-weight: 800;
    background: -webkit-linear-gradient(45deg, #FF6B6B, #4ECDC4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
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

if st.sidebar.button("🚀 RUN SIMULATION", use_container_width=True):
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
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Raw Key Length", results['raw_key_length'], "Qubits Transmitted")
    col2.metric("Sifted Key Length", results['sifted_key_length'], "After Basis Reconciliation")
    col3.metric("Final Key Length", results['estimated_final_key_length'], "Post Privacy Amplification")
    col4.metric("QBER", f"{results['qber']:.2%}", "Quantum Bit Error Rate")
    
    st.subheader("🛡️ Security Status")
    status = results['security_status']
    if "SECURE" in status:
        st.success(f"**{status}**: The QBER is within safe limits. Eve's information has been squeezed out.")
    elif "SUSPICIOUS" in status:
        st.warning(f"**{status}**: Elevated QBER detected. Proceed with extreme caution or abort.")
    else:
        st.error(f"**{status}**: Critical QBER threshold exceeded! Eavesdropper or heavy noise detected. Key aborted.")
        
    st.divider()
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("Raw Data Preview")
        st.code(f"Alice Bits:  {results['alice_bits'][:20]}...\n"
                f"Alice Bases: {results['alice_bases'][:20]}...\n"
                f"Bob Bases:   {results['bob_bases'][:20]}...")
        
    with col_b:
        st.subheader("Example Quantum Circuit")
        if results['example_circuit']:
            st.text(results['example_circuit'].draw(output='text'))
            
    st.divider()
    st.header("📝 Generate Research Paper")
    st.write("Generate an automated, scientifically structured paper draft detailing this exact simulation run.")
    
    paper_markdown = generate_research_paper(results, st.session_state['eve_prob'], st.session_state['noise_prob'], st.session_state['num_bits'])
    
    st.download_button(
        label="📄 Download Research Paper (Markdown)",
        data=paper_markdown,
        file_name="BB84_Research_Analysis.md",
        mime="text/markdown",
        use_container_width=True
    )
    
    with st.expander("Preview Research Paper"):
        st.markdown(paper_markdown)
