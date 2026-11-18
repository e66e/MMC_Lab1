import numpy as np
import matplotlib.pyplot as plt

def main():
    names, ns, times = [], [], []
    with open("czasy.txt") as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            p = line.split()
            names.append(p[0])
            ns.append(int(p[1]))
            times.append(float(p[2]))

    ns    = np.array(ns, dtype=float)
    times = np.array(times, dtype=float)
    per_mln = times / (ns / 1e6)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    bars = ax1.bar(names, times, color="steelblue", edgecolor="black")
    for b, n in zip(bars, ns):
        ax1.text(b.get_x() + b.get_width()/2,
                b.get_height(),
                f"n={int(n):,}",
                ha="center", va="bottom", fontsize=8)
    ax1.set_ylabel("Czas generacji [ms]", fontsize=12)
    ax1.set_title("Całkowity czas pomiaru\n(każdy przebieg ≥ 500 ms)", fontsize=12)
    ax1.grid(axis="y", linestyle=":")

    ax2.bar(names, per_mln, color="indianred", edgecolor="black")
    ax2.set_ylabel("Czas na $10^6$ liczb [ms]", fontsize=12)
    ax2.set_title("Czas unormowany\n(porównywalna miara wydajności)", fontsize=12)
    ax2.grid(axis="y", linestyle=":")

    for ax in (ax1, ax2):
        ax.tick_params(axis="x", rotation=25)
        for lbl in ax.get_xticklabels():
            lbl.set_ha("right")

    plt.tight_layout()
    plt.savefig("wykres_slupkowy.png", format="png", dpi=150)
    plt.show()

if __name__ == "__main__":
    main()