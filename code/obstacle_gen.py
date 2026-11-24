import random
from deap import base, creator, tools, algorithms

# ---------------------------------------------------------------------------
# Level geometry constants. LEVEL_WIDTH and LEVEL_HEIGHT define the tile grid.
# BASE_Y is the default ground row (counted from the top, so row 11 of 15
# puts the ground near the bottom of the screen).
# ---------------------------------------------------------------------------
TILE_AIR   = 0
TILE_SOLID = 11
TILE_BRICK = 2

LEVEL_WIDTH  = 60
LEVEL_HEIGHT = 15
BASE_Y       = 11

NUM_SEGMENTS = 12

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()


def random_segment():
    # ---------------------------------------------------------------------------
    # One segment gene: [platform_width, gap, enemy_type, height_offset].
    # Width 2–8, gap 0–4, enemy 0–2 (0=none, 1=snowball, 2=jumpy), h -2..2.
    # ---------------------------------------------------------------------------
    return [
        random.randint(2, 8),
        random.randint(0, 4),
        random.randint(0, 2),
        random.randint(-2, 2),
    ]


def make_individual():
    genes = []
    for _ in range(NUM_SEGMENTS):
        genes += random_segment()
    return creator.Individual(genes)


toolbox.register("individual", make_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def evaluate(individual):
    # ---------------------------------------------------------------------------
    # Fitness function — higher score = better level.
    #
    # Rewards:
    #   +2  per gap in the jumpable range (1–3 tiles)
    #   +1  per segment with an enemy placed on it
    #   +5  if platform widths are varied (more than 3 distinct values)
    #
    # Penalties:
    #   -10 per platform that exits the vertical playfield (rows 4..13)
    #   -5*(gap-4) per gap wider than 4 tiles (unjumpable for Tux)
    # ---------------------------------------------------------------------------
    score = 0.0
    prev_height = BASE_Y
    gap_sizes = []
    platform_widths = []

    for i in range(0, len(individual), 4):
        p_width, gap, enemy, h_offset = individual[i], individual[i+1], individual[i+2], individual[i+3]
        new_height = prev_height + h_offset

        if new_height < 4 or new_height > LEVEL_HEIGHT - 2:
            score -= 10

        if gap > 4:
            score -= 5 * (gap - 4)

        if 1 <= gap <= 3:
            score += 2

        platform_widths.append(p_width)

        if enemy > 0:
            score += 1

        gap_sizes.append(gap)
        prev_height = new_height

    if len(set(platform_widths)) > 3:
        score += 5

    return (score,)


toolbox.register("evaluate", evaluate)
toolbox.register("mate",    tools.cxTwoPoint)
toolbox.register("mutate",  tools.mutUniformInt, low=-2, up=8, indpb=0.2)
toolbox.register("select",  tools.selTournament, tournsize=3)


def chromosome_to_tilemap(individual):
    grid = [[TILE_AIR] * LEVEL_WIDTH for _ in range(LEVEL_HEIGHT)]
    enemies = []
    x = 2
    cur_y = BASE_Y

    for i in range(0, len(individual), 4):
        p_width, gap, enemy_type, h_offset = individual[i], individual[i+1], individual[i+2], individual[i+3]
        cur_y = max(4, min(LEVEL_HEIGHT - 2, cur_y + h_offset))

        for px in range(x, min(x + p_width, LEVEL_WIDTH)):
            for py in range(cur_y, LEVEL_HEIGHT):
                grid[py][px] = TILE_SOLID


        if enemy_type == 1 and p_width >= 3:
            ex = (x + x + p_width) // 2
            ey = (cur_y - 1) * 32
            enemies.append(f'(snowball (x {ex * 32}) (y {ey}))')
        elif enemy_type == 2 and p_width >= 4:
            ex = (x + x + p_width) // 2
            ey = (cur_y - 1) * 32
            enemies.append(f'(jumpy (x {ex * 32}) (y {ey}))')

        x += p_width + gap
        if x >= LEVEL_WIDTH - 4:
            break

    flat_tiles = [tile for row in grid for tile in row]
    return flat_tiles, enemies, x


def generate_obstacles(seed=None, generations=20, pop_size=50):
    # ---------------------------------------------------------------------------
    # Entry point called by generate_level.py and eval_obstacle_gen.py.
    # Runs the GA for the given number of generations and returns the best
    # individual decoded into a dict the caller can use directly.
    #
    # difficulty is normalised to 0.0–1.0 from the raw fitness score so that
    # generate_level.py has a consistent intensity value regardless of the
    # actual score range the GA produces.
    # ---------------------------------------------------------------------------
    if seed is not None:
        random.seed(seed)

    pop = toolbox.population(n=pop_size)
    hof = tools.HallOfFame(1)

    algorithms.eaSimple(pop, toolbox,
                        cxpb=0.5, mutpb=0.3,
                        ngen=generations,
                        halloffame=hof,
                        verbose=False)

    best = hof[0]
    tiles, enemies, end_x = chromosome_to_tilemap(best)
    fitness_score = best.fitness.values[0]

    difficulty = min(1.0, max(0.0, (fitness_score + 20) / 60))

    return {
        "tiles":      tiles,
        "enemies":    enemies,
        "width":      LEVEL_WIDTH,
        "height":     LEVEL_HEIGHT,
        "spawn_y":    (BASE_Y - 1) * 32,
        "end_x":      end_x * 32,
        "difficulty": difficulty,
    }
