#!/usr/bin/env python3
import os
import random
import time
import math
import shutil
import msvcrt

PHASE1_CHARS = ["o", "O", ".", "●"]
PHASE2_CHARS = ["$", "#", "!", "="]
PHASE3_CHARS = ["|", "¦", "!"]

COLORS = ["\033[91m", "\033[93m", "\033[92m", "\033[96m", "\033[95m"]
RESET = "\033[0m"

MAX_FIREWORKS = 7

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def get_term_size():
    cols, rows = shutil.get_terminal_size((80, 24))
    return max(20, cols), max(10, rows-3)

def render_grid(fireworks, width, height):
    grid = [list(" " * width) for _ in range(height)]
    for fw in fireworks:
        for p in fw["particles"]:
            if not p.get("alive", True):
                continue
            x = int(round(p["x"]))
            y = int(round(p["y"]))
            if 0 <= x < width and 0 <= y < height:
                grid[y][x] = f"{p.get('color','')}{p.get('ch','*')}{RESET}"
    return "\n".join("".join(row) for row in grid)

def create_firework(width, height):
    cx = random.randint(6, max(6, width-6))
    cy = random.randint(3, max(3, height//2))
    particles = []

    # Núcleo central
    particles.append({"x": cx, "y": cy, "ch": "●", "color": random.choice(COLORS), "alive": True})

    # Phase 1 sparks
    n_sparks = random.randint(30, 45)
    for _ in range(n_sparks):
        angle = random.uniform(0, 2*math.pi)
        speed = random.uniform(0.8, 3.0)
        vx = math.cos(angle) * speed
        vy = -math.sin(angle) * speed
        particles.append({
            "x": cx, "y": cy,
            "vx": vx, "vy": vy,
            "ch": random.choice(PHASE1_CHARS),
            "color": random.choice(COLORS),
            "age": 0,
            "alive": True
        })
    return {"particles": particles, "center": (cx, cy), "phase3_done": False}

def update_firework(fw, width, height):
    gravity = 0.12
    any_alive = False
    cx, cy = fw["center"]

    for p in fw["particles"]:
        if not p.get("alive", True):
            continue
        # Phase 1 & 2: moving sparks
        if "vx" in p:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vy"] += gravity
            p["vx"] *= 0.995
            p["age"] += 1
            if p["age"] == 6:
                p["ch"] = random.choice(PHASE2_CHARS)
            if p["age"] > 12:
                p["ch"] = "."
            if p["age"] > 18 or not (0 <= int(round(p["x"])) < width and 0 <= int(round(p["y"])) < height):
                p["alive"] = False
            else:
                any_alive = True
        # Phase 3: rain, spawn after phase2 mostly dead
        elif fw["phase3_done"] == False:
            # spawn short rain particles from center
            for _ in range(random.randint(5, 10)):
                fw["particles"].append({
                    "x": cx + random.uniform(-1.5,1.5),
                    "y": cy,
                    "vy": random.uniform(0.3,0.7),
                    "ch": random.choice(PHASE3_CHARS),
                    "color": random.choice(COLORS),
                    "alive": True
                })
            fw["phase3_done"] = True
        # Update rain particles
        else:
            p["y"] += p.get("vy",0)
            p["vy"] = p.get("vy",0) + 0.05
            if int(round(p["y"])) >= height:
                p["alive"] = False
            else:
                any_alive = True

    return any_alive

def main():
    print("🎆 ASCII Fireworks 3 Phases 🎆")
    print("ENTER para disparar (máx 7 simultáneos), Q para salir.")
    width, height = get_term_size()
    fireworks = []

    try:
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key in [b'\r']:  # ENTER
                    if len(fireworks) < MAX_FIREWORKS:
                        fireworks.append(create_firework(width, height))
                elif key.lower() == b'q':
                    break

            fireworks_alive = []
            for fw in fireworks:
                alive = update_firework(fw, width, height)
                if alive:
                    fireworks_alive.append(fw)
            fireworks = fireworks_alive

            clear()
            print(render_grid(fireworks, width, height))
            time.sleep(0.06)
    except KeyboardInterrupt:
        print("\nBye.")

if __name__ == "__main__":
    main()

