def check_security(qber: float) -> str:
    """
    Determines the security status based on the QBER.
    Standard BB84 aborts if QBER is > ~11%.
    """
    if qber < 0.05:
        return "SECURE / ACCEPT"
    elif qber < 0.11:
        return "SUSPICIOUS"
    else:
        return "COMPROMISED / ABORT"
