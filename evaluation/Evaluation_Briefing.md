# Evaluation Briefing

- `data/fitness_per_gen.csv` — best fitness per generation, across 10 seeds
- `data/summary.csv` — final stats per seed
- `figures/F1_fitness_convergence.png` — the convergence graph
- `figures/level_screenshots/` — screenshots of seeds 0, 42, and 90

---

## To re-run the evaluation from scratch

From `portfolio_2_submission/`:

**1. Install dependencies**
```
pip install -r code/requirements.txt
```

**2. Run the GA across 10 seeds**
```
cd evaluation/scripts
python eval_obstacle_gen.py
```

**3. Generate the convergence graph**
```
python plot_fitness.py
```

---

## GA settings used

| Parameter | Value |
|-----------|-------|
| Population | 50 |
| Generations | 20 |
| Crossover rate | 0.5 |
| Mutation rate | 0.3 |
| Per-gene mutation | 0.2 |
| Selection | Tournament, k=3 |
| Seeds tested | 0, 10, 20, 30, 40, 50, 60, 70, 80, 90 |
