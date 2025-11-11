import numpy

def convolve(a, b):
    size: int = len(a) + len(b) - 1

    result = numpy.empty(size, dtype=float)

    for i in range(0, size):
        sum = 0

        lower = max(i - len(b) + 1, 0)
        upper = min(i + 1, len(a))

        for j in range(lower, upper):
            sum += a[j] * b[i - j]

        result[i] = sum

    return result

# thanks to https://web.cecs.pdx.edu/~maier/cs584/Lectures/lect07b-11-MG.pdf
def recursive_dft(a):
    n = len(a)

    if n == 1:
        return a
    
    principle = numpy.exp(2*numpy.pi*1j/n) # principle nth root of unity
    p = 1.0 + 0.0j # other roots of unity are principle^k

    a0 = [a[i] for i in range(0, n, 2)]
    a1 = [a[i] for i in range(1, n, 2)]

    y0 = recursive_dft(a0)
    y1 = recursive_dft(a1)

    y = numpy.empty(n, numpy.complex128)

    for k in range(0, n // 2 - 1):
        y[k] = y0[k] + p * y1[k]
        y[k + n//2] = y0[k] - p * y1[k]

        p = p * principle

    return y

def fft_convolve(a, b):
    n = len(a)

    principle = numpy.exp(2*numpy.pi*1j/n) # principle root of unity

    p = numpy.empty(n, dtype=complex)
    p[0] = 1.0 + 0.0j
    p[1] = principle

    for i in range(2, n):
        p[i] = p[i - 1] * principle

    f1 = numpy.empty(n, dtype=complex)

    # f1(p[n]) = a * p[n] ^ 0 + b * p[n] ^ 1 ...
    for i in range(n):
        sum = 0.0

        z = 1.0 + 0.0j

        for j in range(n):
            sum += a[j] * z
            z *= p[i]
        f1[i] = sum

    return recursive_dft(f1)

if __name__ == "__main__":
    a = [1, 2, 3, 4, 5, 6, 7, 8]
    b = [9, 10, 11, 12]

    print(convolve(a, b))
    print(fft_convolve(a, b))