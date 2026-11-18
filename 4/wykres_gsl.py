import numpy as np
import matplotlib.pyplot as plt

names, norms, times = [], [], []

with open("czasy_gsl.txt") as f:
    for line in f:
        if line.startswith("#") or not line.strip():
            continue
        p = line.split()
        names.append(p[0])
        times.append(float(p[2]))
        norms.append(float(p[3]))

# Sortowanie rosnąco według czasu unormowanego – czytelniejszy wykres
order = np.argsort(norms)
names  = [names[i]  for i in order]
norms  = [norms[i]  for i in order]
times  = [times[i]  for i in order]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

# --- Panel A: czas unormowany (główny wynik) ---
bars = ax1.barh(names, norms, color="steelblue", edgecolor="black")
ax1.axvline(1.0, color="red", linestyle="--", linewidth=1,
            label="gsl_rng_default = 1.0")
ax1.set_xlabel("Czas unormowany (względem gsl_rng_default)", fontsize=12)
ax1.set_title("Względny czas generacji\n(1.0 = czas generatora domyślnego)", fontsize=12)
ax1.grid(axis="x", linestyle=":")
ax1.legend(fontsize=10)

# Adnotacje z wartościami
for b, v in zip(bars, norms):
    ax1.text(b.get_width() * 1.01, b.get_y() + b.get_height()/2,
             f"{v:.2f}", va="center", fontsize=8)

# --- Panel B: bezwzględny czas pomiaru [ms] ---
ax2.barh(names, times, color="indianred", edgecolor="black")
ax2.set_xlabel("Czas pomiaru [ms]", fontsize=12)
ax2.set_title("Bezwzględny czas generacji\n(każdy przebieg ≥ 500 ms)", fontsize=12)
ax2.grid(axis="x", linestyle=":")

for ax in (ax1, ax2):
    ax.tick_params(axis="y", labelsize=8)

plt.tight_layout()
plt.savefig("wykres_gsl.png", format="png", dpi=150)
plt.show()