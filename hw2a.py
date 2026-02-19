from NumericalMethods import GPDF, Probability


def format_prob_less(mu, sig, c, prob):
    return "P(x<{:0.2f}|N({:0.0f},{:0.0f}))={:0.4f}".format(c, mu, sig, prob)


def format_prob_greater(mu, sig, c, prob):
    return "P(x>{:0.2f}|N({:0.0f},{:0.0f}))={:0.4f}".format(c, mu, sig, prob)


def main():

    mu1 = 100.0
    sig1 = 12.5
    c1 = 105.0

    p_less = Probability(GPDF, (mu1, sig1), c1, GT=False)
    print(format_prob_less(mu1, sig1, c1, p_less))

    mu2 = 100.0
    sig2 = 3.0
    c2 = mu2 + 2 * sig2

    p_greater = Probability(GPDF, (mu2, sig2), c2, GT=True)
    print(format_prob_greater(mu2, sig2, c2, p_greater))


if __name__ == "__main__":
    main()
