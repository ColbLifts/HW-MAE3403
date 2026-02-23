# hw3a.py
from NumericalMethods import Probability, GPDF, Secant

def one_sided_function(mu, sig, targetP, GT):
    """
    Returns a function f(c) = Probability(x<c or x>c)- P
    so we can use the secant function

    """
    def f(c):
        return Probability(GPDF, (mu,sig), c, GT=GT) - targetP
    return f
def two_sided_function(mu, sig, targetP):
    #Two-sided probability P(mu - d <x<mu+d)

    def f(c):
        d= abs(c-mu)
        left =mu - d
        right =mu + d
        p= Probability(GPDF,(mu, sig), right, GT=False)- \
            Probability(GPDF,(mu, sig), left, GT=False)
        return p - targetP
    return f
def main():
    print("===HW3a: Probability <-> c Solver ===")

    mu= float(input("Population mean mu: "))
    sig= float(input("Population standard deviation sigma: "))
    mode = input("Is c or P your input? (c/p):").lower()
    region = input("One sided or two sided? (1/2): ").strip()

    # Case 1: C is given
    if mode == "c":
        c = float(input("Enter c:"))

        if region == "1":
            side = input("Compute P(x<c) or P(x>c)? (< or >):").strip()
            GT = True if side == ">" else False
            p = Probability(GPDF, (mu, sig), c, GT=GT)
            print(f"P(x{side}{c:.3f}|N({mu},{sig})) = {p:.6f}")
        else:
            # two-sided: c defines distance from mu
            d = abs(c-mu)
            left = mu - d
            right = mu + d
            p = Probability(GPDF, (mu, sig), right, GT=False) - \
                Probability(GPDF, (mu, sig), left, GT=False)
            print(f"P({left:.3f} < x < {right:.3f}) = {p:.6f}")

    else:
        targetP = float(input("Enter desired probability P:"))

        if region == "1":
            side = input("Solve for c in P(x<c) or P(x>c)? (< or >):").strip()
            GT = True if side == ">" else False

            f= one_sided_function(mu, sig, targetP, GT)
            c, it = Secant(f, mu-sig, mu + sig, maxiter=20, xtol=1e-6)
            print(f"c={c:.6f} (iterations={it})")

        else:
            f = two_sided_function(mu, sig, targetP)
            c, it = Secant(f, mu - sig, mu + sig, maxiter=20, xtol=1e-6)
            print(f"two-sided c = {c:.6f} (iterations={it})")
if __name__ == "__main__":
    main()
