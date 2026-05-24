# 🎮 Tank Battle 2D

Python + Pygame game project with a clean OOP structure, tile-based map generation, and A* pathfinding.

![Gameplay Demo](docs/gameplay.gif)

## 🚀 Features

- **Advanced Enemy AI:** Enemies use the **A* (A-star) algorithm** for dynamic pathfinding around obstacles, seamlessly switching to direct line-of-sight attacks.
- **Tile-based Environment:** Maps are generated using a tile system (Kenney assets) with dynamic layout changes per level and programmatic color-matching for seamless terrain.
- **In-Game Economy & Upgrades:** Core loop system where score points act as currency to buy tank upgrades (Firepower, Max HP, Speed, Reload Cooldown) via the Pause Menu.
- **Auto-fire & Bouncing Mechanics:** Continuous shooting mechanics and physics-based bullet bouncing off walls.
- **Clean Architecture:** Strict Object-Oriented Programming (OOP) with a modular structure, State Pattern for UI navigation, and separated asset management.

## 📂 Project structure

```text
tank_battle_2d/
├── assets/         # Sprites and tile graphics
├── docs/           # Documentation assets (like gameplay.gif)
├── src/
│   ├── core/       # Core game loops and map generation
│   │   ├── __init__.py
│   │   ├── game.py
│   │   └── game_map.py
│   ├── entities/   # In-game objects
│   │   ├── __init__.py
│   │   ├── bullet.py
│   │   ├── enemy.py
│   │   ├── particle.py
│   │   ├── tank.py
│   │   └── wall.py
│   ├── managers/   # Resource and asset handlers
│   │   ├── __init__.py
│   │   └── assets.py
│   ├── ui/         # User interface and menus
│   │   ├── __init__.py
│   │   ├── button.py
│   │   ├── hud.py
│   │   └── pause_menu.py
│   └── __init__.py
├── .gitignore
├── main.py         # Entry point of the game
├── README.md
├── requirements.txt # Project dependencies
└── settings.py     # Global configurations and constants

```
## 🛠️ Run locally
``` text
# Clone the repository
git clone [https://github.com/YourUsername/tank_battle_2d.git](https://github.com/YourUsername/tank_battle_2d.git)
cd tank_battle_2d

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
