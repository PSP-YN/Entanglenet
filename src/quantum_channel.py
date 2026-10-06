from qiskit_aer.noise import NoiseModel, pauli_error

def get_channel_noise_model(noise_probability: float) -> NoiseModel:
    """
    Creates a simple bit-flip noise model for the quantum channel.
    """
    noise_model = NoiseModel()
    if noise_probability > 0:
        # A simple bit-flip error representing channel noise
        p_error = pauli_error([('X', noise_probability), ('I', 1 - noise_probability)])
        noise_model.add_all_qubit_quantum_error(p_error, ['id', 'x', 'h'])
    return noise_model
