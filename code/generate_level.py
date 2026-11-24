import argparse
import os
import random
import time

from obstacle_gen import generate_obstacles

DEFAULT_MUSIC = "music/chipdisko.ogg"


def build_stl(obstacles, level_name="PCG Level") -> str:
    # ---------------------------------------------------------------------------
    # Assembles the obstacle data into a valid SuperTux v0.6.3 s-expression.
    # TILE_SOLID = 11, TILE_AIR = 0 — tile IDs are baked into the tilemap
    # by chromosome_to_tilemap in obstacle_gen.py before we get here.
    # level_height_px converts tile rows to pixels (32 px per tile) for the
    # sequencetrigger height field.
    # ---------------------------------------------------------------------------
    tilemap_data = " ".join(str(t) for t in obstacles["tiles"])
    enemies_block = "\n    ".join(obstacles["enemies"])
    level_height_px = obstacles["height"] * 32

    stl = f"""(supertux-level
  (version 2)
  (name "{level_name}")
  (author "PCG Generator — Moses")
  (sector
    (name "main")
    (music "{DEFAULT_MUSIC}")
    (tilemap
      (solid #t)
      (speed 1.0)
      (width {obstacles["width"]})
      (height {obstacles["height"]})
      (tiles {tilemap_data})
    )
    (camera
      (mode "normal")
    )
    {enemies_block}
    (spawnpoint
      (name "main")
      (x 64)
      (y {obstacles["spawn_y"]})
    )
    (sequencetrigger
      (sequence "endsequence")
      (width 32)
      (height {level_height_px})
      (x {obstacles["end_x"]})
      (y 0)
    )
  )
)
"""
    return stl


def main():
    parser = argparse.ArgumentParser(description="SuperTux PCG Level Generator — obstacle module")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    parser.add_argument("--out",  type=str, default=None, help="Output .stl file path")
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else int(time.time())
    random.seed(seed)
    print(f"Generating level with seed: {seed}")

    # ---------------------------------------------------------------------------
    # Run the genetic algorithm. generate_obstacles returns the best individual
    # decoded into a tilemap, enemy list, and metadata dict.
    # ---------------------------------------------------------------------------
    print("  Running GA obstacle generator...")
    obstacles = generate_obstacles(seed=seed)

    level_name  = f"PCG Level (seed {seed})"
    stl_content = build_stl(obstacles, level_name)

    tile_count = len(obstacles["tiles"])
    expected   = obstacles["width"] * obstacles["height"]
    assert tile_count == expected, f"Tile count mismatch: got {tile_count}, expected {expected}"

    out_path = args.out or f"output/generated_levels/pcg_seed_{seed}.stl"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        f.write(stl_content)

    print(f"\nLevel written to: {out_path}")
    print(f"Tile count : {tile_count} ({obstacles['width']}x{obstacles['height']}) OK")
    print(f"Difficulty : {obstacles['difficulty']:.2f}")
    print(f"\nTo play:")
    print(f"  supertux2.exe {out_path}")


if __name__ == "__main__":
    main()
