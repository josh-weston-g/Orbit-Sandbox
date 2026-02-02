# Orbit-Sandbox

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg?logo=python&logoColor=ffffff)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-in%20development-yellow.svg)

A physics-accurate Newtonian orbital mechanics simulator built from first principles. Watch planets orbit stars, create elliptical trajectories, or launch escape maneuvers - all emerging naturally from Newton's laws and numerical integration.

> **⚠️ Work in Progress:** This project is actively under development. Features are being added incrementally, and the codebase is evolving. Expect breaking changes and incomplete functionality.
 
## Contents

**Getting Started**
- [What it does](#what-it-does)
- [Installation](#installation)
- [Requirements](#requirements)
- [Usage](#usage)

**Features & Documentation**
- [Current Features](#current-features)
- [Visualization Controls](#visualization-controls)
- [Creating Custom Systems](#creating-custom-systems)

**Technical Details**
- [Project Structure](#project-structure)
- [How it Works](#how-it-works)

**Project Info**
- [Known Limitations & Future Work](#known-limitations--future-work)
- [Contributing](#contributing)
- [License](#license)
- [Assets & Credits](#assets--credits)
- [Author](#author)

## What it does

Orbit-Sandbox simulates gravitational interactions between celestial bodies using real Newtonian N-body physics. All bodies attract each other according to Newton's law of universal gravitation, and the system evolves forward (and backward!) in time using Velocity Verlet integration.

Systems are defined in JSON files, making it easy to create and share custom orbital configurations. The simulator comes with 7 pre-built systems including binary stars, three-body configurations, and the complete solar system.

The interactive Pygame visualization provides real-time rendering with zoom, pan, orbital trails, and time manipulation including pause and rewind. Whether you want to explore orbital mechanics, watch a three-body system's chaotic evolution, or rewind the solar system, Orbit-Sandbox provides an honest physics engine that behaves like the real universe.

## Current Features

- 🪐 **Seven pre-built systems:** Binary stars, Sun-Earth orbit, elliptical orbit, escape trajectory, three-body triangle, inner solar system, and complete solar system (Mercury to Neptune)
- ⚙️ **N-body physics:** Full gravitational interactions between all bodies, Velocity Verlet integration (2nd order), excellent energy/momentum conservation, rewind capability
- 🎮 **Interactive visualization:** Real-time rendering with pygame_gui menus, dynamic resolution, zoom/pan controls, toggleable grid and trails, pause/rewind, real-time HUD
- 📁 **JSON-based systems:** Create custom systems without coding - drop JSON files in `data/systems/` and they appear automatically
- 🎯 **Modular architecture:** Clean separation between physics, simulation, UI views, and rendering

## Project Structure

The codebase is organized with clear separation of concerns:

```
Orbit-Sandbox/
├── main.py                # Entry point - main loop, view management, resolution handling
├── requirements.txt       # Python dependencies
├── assets/
│   ├── fonts/             # JetBrains Mono Nerd Font (Regular and Bold)
│   ├── images/            # Images used in the app (Menu Background, etc.)
│   └── themes/            # JSON files defining styles for menu components
├── data/
│   ├── default_systems/   # JSON default system definitions
│   │   ├── binary_stars.json
│   │   ├── circular_orbit.json
│   │   ├── elliptical_orbit.json
│   │   ├── escape_trajectory.json
│   │   ├── three_body_triangle.json
│   │   ├── solar_system_inner.json
│   │   └── solar_system.json
│   └── custom_systems/    # User-created custom systems
├── orbit/
│   ├── __init__.py
│   ├── body.py            # Body class - position, velocity, acceleration, mass, name
│   ├── physics.py         # Gravity calculations and orbital velocity formulas
│   ├── simulation.py      # Simulation class - N-body physics, integration, time stepping, rewind
│   ├── loader.py          # SystemLoader - loads systems from JSON files
│   └── units.py           # Unit conversions and constants (AU, years, G)
└── ui/
    ├── __init__.py
    ├── views.py           # UI views using pygame_gui (MainMenuView, LoadSystemView, SimulationView)
    └── visualize.py       # SimulationRunner class - physics updates, rendering, controls
```

Core classes:
- **Body:** Represents a physical object with position, velocity, acceleration, mass, name, and type
- **Simulation:** Orchestrates the N-body physics loop, Velocity Verlet integration, state history, and time manipulation
- **SystemLoader:** Loads orbital systems from JSON files and discovers available systems
- **Views:** Frame-based UI screens using pygame_gui (MainMenuView, LoadSystemView, SimulationView)
- **SimulationRunner:** Handles simulation logic, physics updates, rendering, and user controls

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/josh-weston-g/Orbit-Sandbox.git
   cd Orbit-Sandbox
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
   > **Note:** Use Python 3.12 or 3.13. Python 3.14 has compatibility issues with pygame.

3. **Install Dependencies:**
    ```bash
      pip install -r requirements.txt
    ```

## Requirements

- **Python 3.12 or 3.13** (Python 3.14 not yet supported due to pygame compatibility issues)
- NumPy
- Pygame
- pygame-gui

## Usage

```bash
# Run with default settings (auto-detect resolution)
python main.py

# Specify window resolution
python main.py --resolution 720p
python main.py --resolution 1080p
python main.py --resolution 1440p
```

Available resolutions:
- `auto` - Auto-detect display size and use borderless fullscreen (default)
- `720p` - 1280×720 window
- `1080p` - 1920×1080 window
- `1440p` - 2560×1440 window

The application launches with a **dynamic menu** showing all available systems from the `data/systems/` directory. Click any system to load and run it.

### Visualization Controls

**Camera:**
- **Mouse wheel:** Zoom in/out
- **WASD keys:** Pan camera (up/left/down/right)
- **Click and drag:** Pan camera with mouse

**Visualization Toggles:**
- **G:** Toggle grid overlay (0.5 AU spacing)
- **T:** Toggle orbital trails
- **E:** Toggle energy display in HUD

**Time Control:**
- **Spacebar:** Pause/resume simulation
- **LEFT arrow:** Rewind simulation
- **R:** Reset simulation to initial conditions
- **UP/DOWN arrows:** Adjust simulation speed multiplier

**Navigation:**
- **ESC:** Return to system selection menu

### Creating Custom Systems

Create a JSON file in `data/systems/` with this format:

```json
{
  "name": "My Custom System",
  "description": "A brief description of the system",
  "G": 39.478 # Optional
  "bodies": [
    {
      "mass": 1.0,
      "position": [0, 0],
      "velocity": [0, 0],
      "name": "Central Star",
      "type": "star"
    },
    {
      "mass": 3.0e-6,
      "position": [1.0, 0],
      "velocity": [0, 6.283185],
      "name": "Planet",
      "type": "planet"
    }
  ]
}
```

**Units:**
- Mass: Solar masses (Sun = 1.0, Earth ≈ 3×10⁻⁶)
- Position: AU (Astronomical Units, Earth-Sun distance = 1.0)
- Velocity: AU/year (Earth's orbital speed ≈ 6.28)
- G defaults to 39.478 AU³/(M☉·year²) if not specified

The system will automatically appear in the menu on the next launch. Use the circular orbit velocity formula for stable orbits: `v = sqrt(G * M / r)` where M is the central mass and r is the orbital radius.

## How it Works

### N-Body Physics Engine

The simulation implements full N-body gravitational dynamics where every body attracts every other body according to Newton's law of universal gravitation:

```
F = G * m1 * m2 / r²
```

For each body, the total acceleration is computed by summing gravitational forces from all other bodies:

```python
def _compute_total_acceleration(self, body):
    """Compute total gravitational acceleration on a body from all other bodies."""
    total_accel = np.zeros(2, dtype=float)
    
    for other in self.bodies:
        if other is not body:  # Skip self
            total_acc += compute_acceleration(body, other, self.G)
    
    return total_acc
```

### Velocity Verlet Integration

The simulator uses **Velocity Verlet integration** (2nd order accuracy) to update positions and velocities:

```python
# Phase 1: Calculate old accelerations for all bodies
for body in self.bodies:
    body.old_acc = self._compute_total_acceleration(body)

# Phase 2: Update all positions using old acceleratio
for body in self.bodies:
    body.pos += body.vel * dt + 0.5 * body.old_acc * dt²

# Phase 3: Calculate new acceleration for all bodies at updated positions
for body in self.bodies:
    body.new_acc = self._compute_total_acceleration(body)

# Phase 4: Update all velocities using average of old and new accelerations
for body in self.bodies:
    body.vel += 0.5 * (body.old_acc + body.new_acc) * dt
    body.acc = body.new_acc
```

This method evaluates acceleration at both the start and end of each timestep, using their average for velocity updates. This provides 2nd-order accuracy and excellent long-term energy conservation, keeping orbits stable over thousands of orbits.

### Rewind Capability

The simulator maintains a limited state history, allowing full rewind functionality:

```python
def save_state(self):
    """Save current state to history for rewind capability."""
    state = [(body.pos.copy(), body.vel.copy()) for body in self.bodies]
    self.history.append(state)

def rewind_one_step(self):
    """Rewind simulation by one step."""
    if len(self.state_history) > 1:
        self.history.pop()  # Remove current state
        state = self.history[-1]  # Get previous state
        for i, body in enumerate(self.bodies):
            body.pos, body.vel = state[i][0].copy(), state[i][1].copy()
```
> **Note**: The length of the state history can be changed by changing `self.max_history` in `simulation.py`

### Energy Conservation

The simulation displays total mechanical energy (kinetic + potential) as a diagnostic tool. In a perfect orbital system, total energy should remain constant. Thanks to the Velocity Verlet integrator (2nd order accuracy), energy is conserved to within ~0.01% over thousands of orbits - a 200x improvement over basic Euler methods. This excellent conservation allows the simulation to run stably for extended periods without drift, even in chaotic multi-body systems.

## Known Limitations & Future Work

**Current limitations:**
- 2D simulation (no z-axis)
- Fixed timestep (not adaptive)
- No collision detection
- No relativistic effects

**Planned features:**
- Body colors in JSON (override default color palette)
- Visual system builder (create systems with mouse clicks)
- Body labels and selection (click to highlight, show info)
- Camera follow modes (follow specific bodies or barycenter)
- Additional integration methods (RK4, adaptive timestep)
- More scenario presets (Lagrange points, figure-8 orbits, Pluto)
- Pause menu (in-sim menu with settings, quit options)
- Trajectory prediction (show future path)

## Contributing

This is a learning project and contributions are welcome! If you'd like to contribute:

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a Pull Request

Since this is a work in progress, feel free to open issues with ideas, bugs, or questions about the physics implementation.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Assets & Credits

#### Images 
- Menu Background: [Vecteezy](https://www.vecteezy.com/free-photos/space)

#### Fonts
- JetBrains Mono Nerd Font: [Nerd Fonts](https://www.nerdfonts.com/)

## Author

Josh Weston - [@josh-weston-g](https://github.com/josh-weston-g)
