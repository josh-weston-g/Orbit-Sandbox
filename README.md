# Orbit-Sandbox

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg?logo=python&logoColor=ffffff)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-in%20development-yellow.svg)

A physics-accurate Newtonian orbital mechanics simulator built from first principles. Watch planets orbit stars, create elliptical trajectories, or launch escape maneuvers - all emerging naturally from Newton's laws and numerical integration.

> **⚠️ Work in Progress:** This project is actively under development. Features are being added incrementally, and the codebase is evolving. Expect breaking changes and incomplete functionality.

## What it does

Orbit-Sandbox simulates gravitational interactions between celestial bodies using real Newtonian N-body physics. All bodies attract each other according to Newton's law of universal gravitation, and the system evolves forward (and backward!) in time using Velocity Verlet integration.

Systems are defined in JSON files, making it easy to create and share custom orbital configurations. The simulator comes with 7 pre-built systems including binary stars, three-body configurations, and the complete solar system.

The interactive Pygame visualization provides real-time rendering with zoom, pan, orbital trails, and time manipulation including pause and rewind. Whether you want to explore orbital mechanics, watch a three-body system's chaotic evolution, or rewind the solar system, Orbit-Sandbox provides an honest physics engine that behaves like the real universe.

## Current Features

- 🪐 **Seven pre-built systems:**
  - Binary Stars - Two equal-mass stars orbiting their barycenter
  - Sun-Earth Orbit - Earth in perfect circular orbit around the Sun
  - Elliptical Orbit - Earth in elliptical orbit (70% circular velocity)
  - Escape Trajectory - Earth escaping the Sun's gravity
  - Three-Body Triangle - Three equal masses in rotating equilateral configuration
  - Inner Solar System - Sun with Mercury, Venus, Earth, and Mars
  - Complete Solar System - All 8 planets from Mercury to Neptune
- ⚙️ **N-body physics simulation:**
  - Full N-body gravity (all bodies attract each other)
  - Newtonian gravity (inverse square law)
  - Velocity Verlet integration (2nd order accuracy)
  - Excellent energy conservation
  - Conserves angular momentum
  - Rewind capability with full state history
- 🎮 **Interactive visualization:**
  - Real-time Pygame rendering
  - Dynamic menu system
  - Dynamic window resolution (auto-detection or fixed sizes)
  - Mouse wheel zoom
  - Camera panning with WASD keys or click-and-drag
  - Toggleable grid overlay
  - Orbital trail rendering
  - Pause/resume with spacebar
  - Rewind simulation
  - Reset simulation with R key
  - ESC to return to menu
  - Real-time HUD with time, speed, scale, and energy display
- 📁 **JSON-based system definitions:**
  - Easy to create custom systems without coding
  - Human-readable format with mass, position, velocity for each body
  - Optional body names and types (star, planet, body)
  - Drop JSON files in `data/systems/` and they appear in the menu automatically
- 🎯 **Modular architecture:**
  - Clean separation between physics, simulation, data, and rendering
  - Easy to extend with new systems or integrators

## Project Structure

The codebase is organized with clear separation of concerns:

```
Orbit-Sandbox/
├── main.py                # Entry point - resolution argument handling
├── requirements.txt       # Python dependencies
├── assets/
│   └── fonts/             # JetBrains Mono Nerd Font (Regular and Bold)
├── data/
│   └── systems/           # JSON system definitions
│       ├── binary_stars.json
│       ├── circular_orbit.json
│       ├── elliptical_orbit.json
│       ├── escape_trajectory.json
│       ├── three_body_triangle.json
│       ├── solar_system_inner.json
│       └── solar_system.json
├── orbit/
│   ├── __init__.py
│   ├── body.py            # Body class - position, velocity, acceleration, mass, name
│   ├── physics.py         # Gravity calculations and orbital velocity formulas
│   ├── simulation.py      # Simulation class - N-body physics, integration, time stepping, rewind
│   ├── loader.py          # SystemLoader - loads systems from JSON files
│   └── units.py           # Unit conversions and constants (AU, years, G)
└── ui/
    ├── __init__.py
    └── visualize.py       # Pygame visualization, dynamic menu, and user input handling
```

Core classes:
- **Body:** Represents a physical object with position, velocity, acceleration, mass, name, and type
- **Simulation:** Orchestrates the N-body physics loop, Velocity Verlet integration, state history, and time manipulation
- **SystemLoader:** Loads orbital systems from JSON files and discovers available systems
- **Visualization:** Handles Pygame rendering, dynamic menu generation, and interactive controls

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

## Requirements

- **Python 3.12 or 3.13** (Python 3.14 not yet supported due to pygame compatibility issues)
- NumPy
- Pygame

## How it Works

### N-Body Physics Engine

The simulation implements full N-body gravitational dynamics where every body attracts every other body according to Newton's law of universal gravitation:

```
F = G * m1 * m2 / r²
```

For each body, the total acceleration is computed by summing gravitational forces from all other bodies:

```python
def _compute_total_acceleration(self, body_index):
    """Compute total gravitational acceleration on a body from all other bodies."""
    total_accel = np.array([0.0, 0.0])
    body = self.bodies[body_index]
    
    for i, other_body in enumerate(self.bodies):
        if i != body_index:
            accel = compute_acceleration(body, other_body, self.G)
            total_accel += accel
    
    return total_accel
```

### Velocity Verlet Integration

The simulator uses **Velocity Verlet integration** (2nd order accuracy) to update positions and velocities:

```python
# 1. Calculate acceleration at current position for all bodies
old_accelerations = [compute_total_acceleration(i) for i in range(n)]

# 2. Update positions with half-step correction
for i, body in enumerate(bodies):
    body.pos += body.vel * dt + 0.5 * old_accelerations[i] * dt²

# 3. Calculate acceleration at new positions
new_accelerations = [compute_total_acceleration(i) for i in range(n)]

# 4. Update velocities using average acceleration
for i, body in enumerate(bodies):
    body.vel += 0.5 * (old_accelerations[i] + new_accelerations[i]) * dt
```

This method evaluates acceleration at both the start and end of each timestep, using their average for velocity updates. This provides 2nd-order accuracy and excellent long-term energy conservation, keeping orbits stable over thousands of orbits.

### Rewind Capability

The simulator maintains a limited state history, allowing full rewind functionality:

```python
def save_state(self):
    """Save current state to history for rewind capability."""
    state = [(body.pos.copy(), body.vel.copy()) for body in self.bodies]
    self.state_history.append(state)

def rewind_one_step(self):
    """Rewind simulation by one step."""
    if len(self.state_history) > 1:
        self.state_history.pop()  # Remove current state
        state = self.state_history[-1]  # Get previous state
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
- Improved menu system
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

## Author

Josh Weston - [@josh-weston-g](https://github.com/josh-weston-g)