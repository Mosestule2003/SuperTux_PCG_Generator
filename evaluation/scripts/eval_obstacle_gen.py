# ---------------------------------------------------------------------------
# eval_obstacle_gen.py
# Evaluates the genetic algorithm in obstacle_gen.py across multiple seeds.
#
# Runs the GA end-to-end for each seed in SEEDS, recording the best fitness
# at every generation.
# ---------------------------------------------------------------------------

import sys
import os
import csv
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "code"))

import obstacle_gen
from deap import tools, algorithms

SEEDS = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]

FITNESS_CSV = os.path.join(os.path.dirname(__file__), "..", "data", "fitness_per_gen.csv")
SUMMARY_CSV = os.path.join(os.path.dirname(__file__), "..", "data", "summary.csv")


def run_one_seed(seed):
   
    tb = obstacle_gen.toolbox
    random.seed(seed)
    pop = tb.population(n=50)
    hof = tools.HallOfFame(1)
    best_per_gen = []

    for gen in range(20):
        pop, log = algorithms.eaSimple(pop, tb, cxpb=0.5, mutpb=0.3,
                                       ngen=1, halloffame=hof, verbose=False)
        best_per_gen.append(hof[0].fitness.values[0])

    final_best = hof[0].fitness.values[0]
    all_fit = [ind.fitness.values[0] for ind in pop]
    avg   = sum(all_fit) / len(all_fit)
    worst = min(all_fit)
    return best_per_gen, final_best, avg, worst


def main():

    out_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(out_dir, exist_ok=True)

    all_gen_rows     = []
    all_summary_rows = []

    for seed in SEEDS:
        print("Running seed", seed)
        best_per_gen, final_best, avg, worst = run_one_seed(seed)
        for gen, fit in enumerate(best_per_gen):
            all_gen_rows.append([seed, gen + 1, fit])
        all_summary_rows.append([seed, final_best, avg, worst])

    with open(FITNESS_CSV, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["seed", "generation", "best_fitness"])
        w.writerows(all_gen_rows)

    with open(SUMMARY_CSV, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["seed", "best_fitness", "avg_fitness", "worst_fitness"])
        w.writerows(all_summary_rows)

    print("Done. Files saved to", out_dir)


if __name__ == "__main__":
    main()
