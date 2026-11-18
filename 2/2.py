import numpy as np
import matplotlib.pyplot as plt

m1, a1 = 30269, 171
m2, a2 = 30307, 172
m3, a3 = 30323, 170

def wichmann_hill(N, seed=(1, 2, 3), burn_in=1000):
    x, y, z = seed
    x %= m1
    y %= m2
    z %= m3

    # rozbieg generatora
    # for _ in range(burn_in):
    #     x = (a1 * x) % m1
    #     y = (a2 * y) % m2
    #     z = (a3 * z) % m3

    K = np.empty(N, dtype=np.float64)
    for i in range(N):
        x = (a1 * x) % m1
        y = (a2 * y) % m2
        z = (a3 * z) % m3
        K[i] = (x / m1 + y / m2 + z / m3) % 1.0
    return K


def rysuj_strukture(K, lag, nazwa_pliku):
    X = K[:-lag]
    Y = K[lag:]

    np.savetxt(
        nazwa_pliku + ".txt",
        np.column_stack((X, Y)),
        fmt="%.17g"
    )

    plt.figure(figsize=(7, 7))
    plt.scatter(X, Y, s=0.2, alpha=0.25, rasterized=True)
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.gca().set_aspect("equal")
    plt.xlabel(r"$k_n$", fontsize=13)
    plt.ylabel(rf"$k_{{n+{lag}}}$", fontsize=13)
    plt.title(f"Wichmann–Hill, pary $(k_n,k_{{n+{lag}}})$", fontsize=13)
    plt.grid(linestyle=":")
    plt.savefig(nazwa_pliku + ".png", format="png", bbox_inches="tight")
    plt.show()

def main():
    N = 500_000
    K = wichmann_hill(N)

    rysuj_strukture(K, lag=1, nazwa_pliku="wh_lag1")
    rysuj_strukture(K, lag=2, nazwa_pliku="wh_lag2")

if __name__ == "__name__":
    main()