from math import gamma, sqrt, pi

def simpson_general(f, a, b, N=800):
    if N % 2 == 1:
        N += 1
    h = (b - a) / N
    total = f(a) + f(b)
    for k in range(1, N):
        x = a + k*h
        total += (4 if k % 2 else 2) * f(x)
    return (h/3) * total

def t_pdf(u, m):
    return (1 + (u*u)/m) ** (-(m+1)/2)

def Km(m):
    return gamma((m+1)/2) / (sqrt(m*pi) * gamma(m/2))

def t_cdf(z, m):
    left = -50
    def pdf(u):
        return Km(m) * t_pdf(u, m)
    return simpson_general(pdf, left, z, N=800)

def main():
    print("=== HW3b: T-distribution ===")
    m = int(input("Degrees of freedom (m): "))
    z = float(input("Value of z: "))
    F = t_cdf(z, m)
    print(f"F(z) for m={m}, z={z:.3f} is approximately {F:.6f}")

if __name__ == "__main__":
    main()
