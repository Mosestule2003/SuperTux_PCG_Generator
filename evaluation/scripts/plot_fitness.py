# ---------------------------------------------------------------------------
# plot_fitness.py
# Reads fitness_per_gen.csv and produces the fitness convergence figure.
#
# Each seed is plotted as a thin grey line; the average across all seeds
# is plotted as a bold blue line. 
# ---------------------------------------------------------------------------

import csv
import os
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Input and output paths are relative to this script's location so the
# script works regardless of the working directory it is run from.
# ---------------------------------------------------------------------------
FITNESS_CSV = os.path.join(os.path.dirname(__file__), "..", "data", "fitness_per_gen.csv")
OUT_PNG     = os.path.join(os.path.dirname(__file__), "..", "figures", "F1_fitness_convergence.png")


def main():
  
    seeds = []
    data  = {}

    with open(FITNESS_CSV, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            seed = int(row["seed"])
            fit  = float(row["best_fitness"])
            if seed not in data:
                data[seed] = []
                seeds.append(seed)
            data[seed].append(fit)

    num_gen = len(list(data.values())[0])
    gens    = list(range(1, num_gen + 1))

    avg_per_gen = []
    for g in range(num_gen):
        vals = [data[s][g] for s in seeds]
        avg_per_gen.append(sum(vals) / len(vals))

    plt.figure(figsize=(8, 5))

    for s in seeds:
        plt.plot(gens, data[s], color="grey", linewidth=0.8, alpha=0.5)

    plt.plot(gens, avg_per_gen, color="blue", linewidth=2, label="Average across seeds")

    plt.xlabel("Generation")
    plt.ylabel("Best Fitness")
    plt.title("Fitness Convergence Over Generations")
    plt.legend()
    plt.tight_layout()

    out_dir = os.path.dirname(OUT_PNG)
    os.makedirs(out_dir, exist_ok=True)
    plt.savefig(OUT_PNG, dpi=150)
    print("Saved to", OUT_PNG)


if __name__ == "__main__":
    main()
