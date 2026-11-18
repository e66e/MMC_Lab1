import numpy as np
import matplotlib.pyplot as plt

m = 2**13 - 1
N = 2500
x0 = 1

def gen_multiplicative(a, n=N, m=m, x0=x0):
    x = np.empty(n, dtype=np.int64)
    x[0] = x0 % m
    for i in range(1, n):
        x[i] = (a * x[i-1]) % m
    return x

def save_and_draw(a, lag):
    x = gen_multiplicative(a)
    X = x[:-lag]
    Y = x[lag:]
    fname = f"dane_a{a}_lag{lag}.txt"
    np.savetxt(fname, np.column_stack((X, Y)), fmt="%d")

    plt.figure(figsize=(6, 6))
    plt.plot(X, Y, ".", markersize=1)
    plt.xlabel("x_n", fontsize=12)
    plt.ylabel(f"x_(n+{lag})", fontsize=12)
    plt.title(f"a={a}, krok={lag}")
    plt.grid(linestyle=":")
    plt.axis("equal")
    plt.savefig(f"wykres_a{a}_lag{lag}.png", format="png")
    plt.show()

def main():
    for a in (17, 85):
        for lag in (1, 2):
            save_and_draw(a, lag)

if __name__ == "__main__":
    main()