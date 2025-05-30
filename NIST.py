import math
from scipy.stats import chi2
'''
THIS IS NOT A COMPLETE NIST TEST SUITE
Contents:
    - Approximate entropy test
    - Serial test
'''

def approximate_entropy_test(bits: str, m: int):
    """
    Performs the NIST Approximate Entropy Test on a binary sequence.

    Args:
        bits: The input binary sequence as a string of '0' and '1'.
        m: Block length for the test.

    Returns:
        A tuple (ApEn, chi_squared, p_value).
        - ApEn: The approximate entropy value.
        - chi_squared: Test statistic.
        - p_value: Corresponding p-value.
    """
    n = len(bits)
    # Form extended sequence (wrap-around) for blocks of length m+1
    ext = bits + bits[:m+1 - 1]

    def _phi(m_len):
        counts = {}
        for i in range(n):
            block = ext[i:i + m_len]
            counts[block] = counts.get(block, 0) + 1
        # compute phi
        total = 0.0
        for count in counts.values():
            freq = count / n
            total += freq * math.log(freq)
        return total

    phi_m = _phi(m)
    phi_m1 = _phi(m + 1)

    ApEn = phi_m - phi_m1
    chi_squared = 2.0 * n * (math.log(2) - ApEn)
    df = 2 ** (m - 1)
    p_value = chi2.sf(chi_squared, df)
    return ApEn, chi_squared, p_value


def serial_test(bits: str, m: int):
    """
    Performs the NIST Serial Test on a binary sequence.

    Args:
        bits: The input binary sequence as a string of '0' and '1'.
        m: Block length for the test.

    Returns:
        A tuple (psi_m, psi_m1, psi_m2, p_value).
        - psi_m, psi_m1, psi_m2: The psi^2 statistics for m, m-1, and adjusted.
        - p_value: Corresponding p-value for the serial test.
    """
    n = len(bits)
    ext = bits + bits[:m - 1]

    def _psi(m_len):
        counts = {}
        for i in range(n):
            block = ext[i:i + m_len]
            counts[block] = counts.get(block, 0) + 1
        psi = 0.0
        for count in counts.values():
            psi += count ** 2
        psi = (psi * (2 ** m_len) / n) - n
        return psi

    psi_m = _psi(m)
    psi_m1 = _psi(m - 1)
    psi_m2 = psi_m - psi_m1

    df = 2 ** (m - 1) - 1
    p_value = chi2.sf(psi_m2, df)
    return psi_m, psi_m1, psi_m2, p_value

if __name__ == "__main__":
    # Example usage
    test_seq = '01010101011110011010'
    m_val = 3
    print("Approximate Entropy Test:")
    ApEn, chi2_stat, p = approximate_entropy_test(test_seq, m_val)
    print(f"ApEn: {ApEn:.6f}, chi2: {chi2_stat:.6f}, p-value: {p:.6f}")

    print("\nSerial Test:")
    psi_m, psi_m1, psi_m2, p2 = serial_test(test_seq, m_val)
    print(f"psi_m: {psi_m:.6f}, psi_m1: {psi_m1:.6f}, psi_m2: {psi_m2:.6f}, p-value: {p2:.6f}")
