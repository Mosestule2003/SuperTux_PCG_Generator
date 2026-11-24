# Obstacle Generation — PCG Portfolio 2

**Course:** COMP 4980 — Game Development  
**Institution:** Thompson Rivers University  
**Student:** Moses Kpughur-Tule  
**TRU ID:** T00721068  
**Date:** November 2026

---

## Overview

This is part of a group final project where my team is building a full Procedural Content Generation (PCG) system for the open-source platformer SuperTux. The project has three parts: obstacle generation (my part), background generation (Daniel), and music generation (Magdala). Each of us is submitting our own component separately for Portfolio 2. This folder is my individual submission — it's self-contained and everything runs directly from here.

The core of my component is a Genetic Algorithm (GA) built with the DEAP library that procedurally generates obstacle layouts for SuperTux levels. Instead of hand-designing platforms, gaps, and enemies, the algorithm evolves them automatically over 20 generations. I ran evaluations across 10 different random seeds to show that it works consistently.

---

## What you need

- Python 3.9 or higher (tested on 3.11)
- SuperTux 0.6.3 — to play the generated levels (download from https://www.supertux.org/)

---

## Setup

**1. Clone the repo**

```
git clone <repo-url>
cd portfolio_2_submission
```

**2. Install dependencies**

```
pip install -r code/requirements.txt
```

---

## Generating a level

From inside `portfolio_2_submission`:

```
cd code
python generate_level.py --seed 42
```

The level file will be saved to:

```
code/output/generated_levels/pcg_seed_42.stl
```

You can use any integer as the seed. Try `0`, `42`, or `90` to reproduce the levels I evaluated.

---

## Playing a generated level

After generating, open it in SuperTux:

**Windows:**
```
"C:\Program Files\SuperTux\bin\supertux2.exe" "code\output\generated_levels\pcg_seed_42.stl"
```

**Mac / Linux:**
```
supertux2 code/output/generated_levels/pcg_seed_42.stl
```

Screenshots of what seeds 0, 42, and 90 look like are in `evaluation/figures/level_screenshots/`.

---

## Running the evaluation

The evaluation scripts test the GA across 10 seeds and generate the convergence graph.

```
cd evaluation/scripts
python eval_obstacle_gen.py
python plot_fitness.py
```

**What `eval_obstacle_gen.py` does:**

Runs the GA 10 times with seeds `[0, 10, 20, 30, 40, 50, 60, 70, 80, 90]`. After each run it records the best fitness at every generation and writes two files:

- `evaluation/data/fitness_per_gen.csv` — 200 rows (10 seeds × 20 generations). Columns: `seed`, `generation`, `best_fitness`.
- `evaluation/data/summary.csv` — 10 rows, one per seed. Columns: `seed`, `best_fitness`, `avg_fitness`, `worst_fitness`.

**What `plot_fitness.py` does:**

Reads `fitness_per_gen.csv` and generates the convergence graph. Each seed is a thin grey line; the average across all seeds is the bold blue line. Saves to:

- `evaluation/figures/F1_fitness_convergence.png`

Note: both CSV files and the graph are already included so you don't have to re-run the evaluation to see the results.

---

## GA settings

These are defined at the top of `code/obstacle_gen.py`:

| Setting | Value | What it means |
|---|---|---|
| `LEVEL_WIDTH` | 60 | Tile columns per row |
| `LEVEL_HEIGHT` | 15 | Tile rows in the level |
| `BASE_Y` | 11 | Ground row (0-indexed from top) |
| `TILE_SOLID` | 11 | SuperTux tile ID for a solid block |
| `TILE_AIR` | 0 | Empty space tile ID |
| Population size | 50 | Candidates per generation |
| Generations | 20 | How long the algorithm runs |
| Crossover rate | 0.5 | Probability two parents swap genes |
| Mutation rate | 0.3 | Probability an individual mutates |
| Selection | Tournament, k=3 | How the best candidates are chosen |

---

## How the fitness function works

The fitness function in `obstacle_gen.py` scores each candidate layout on:

- **Platforms** — isolated solid tiles the player can jump on
- **Gaps** — air gaps between platforms (adds challenge)
- **Enemies** — enemy tiles placed on platforms
- **Wall penalty** — unbroken walls that make the level unpassable get a heavy deduction

A score around 40 is a well-structured, playable layout.

---

## Folder structure

```
portfolio_2_submission/
├── README.md
├── code/
│   ├── obstacle_gen.py          # the GA — my main component
│   ├── generate_level.py        # assembles the full .stl level file
│   ├── requirements.txt
│   └── output/
│       └── generated_levels/    # .stl files go here when you run generate_level.py
├── evaluation/
│   ├── EVALUATION_BRIEFING.md   # how to read and reproduce the evaluation
│   ├── scripts/
│   │   ├── eval_obstacle_gen.py # runs GA across 10 seeds
│   │   └── plot_fitness.py      # generates convergence graph
│   ├── data/
│   │   ├── fitness_per_gen.csv  # 200 rows — best fitness per gen per seed
│   │   └── summary.csv          # 10 rows — final stats per seed
│   └── figures/
│       ├── F1_fitness_convergence.png
│       └── level_screenshots/
│           ├── level_seed_0.jpg
│           ├── level_seed_42.jpg
│           └── level_seed_90.jpg
└── report/
    └── moses_obstacle_pcg_report.md
```

---

## Results

| Seed | Best Fitness | Avg Fitness | Worst Fitness |
|------|-------------|-------------|---------------|
| 0    | 40.0        | 19.70       | -83.0         |
| 10   | 41.0        | 16.30       | -97.0         |
| 20   | 38.0        | 21.54       | -118.0        |
| 30   | 39.0        | 20.08       | -83.0         |
| 40   | 39.0        | 17.66       | -100.0        |
| 50   | 41.0        | 10.94       | -92.0         |
| 60   | 39.0        | 19.40       | -95.0         |
| 70   | 41.0        | 28.58       | -90.0         |
| 80   | 38.0        | 12.60       | -95.0         |
| 90   | 38.0        | 15.06       | -102.0        |

Best individual reached **41.0** (seeds 10, 50, 70). Average best across all seeds: **39.4**.

---

## Status

Everything is done. The evaluation has been run, both CSV files are saved, and the convergence graph is generated. Levels have been tested in SuperTux 0.6.3. See `report/moses_obstacle_pcg_report.md` for the full write-up.
