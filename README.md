# Orbit-Sandbox

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg?logo=python&logoColor=ffffff)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-in%20development-yellow.svg)

A physics-accurate Newtonian orbital mechanics simulator built from first principles. Watch planets orbit stars, create elliptical trajectories, or launch escape maneuvers - all emerging naturally from Newton's laws and numerical integration.

> **⚠️ Work in Progress:** This project is actively under development. Features are being added incrementally, and the codebase is evolving. Expect breaking changes and incomplete functionality.

## What it does

Orbit-Sandbox simulates gravitational interactions between celestial bodies using real Newtonian physics - no predetermined paths, no fake orbits. You set initial conditions (position, velocity, mass), and the simulator evolves the system forward in time using semi-implicit Euler integration. Orbital paths emerge naturally from the underlying forces.

The simulator can run in two modes:
- **Console mode:** Outputs orbital data to the terminal with periodic position/velocity updates
- **Visualization mode:** Interactive Pygame window with real-time rendering, zoom controls, and orbital trails

Whether you want to explore orbital mechanics, experiment with different initial conditions, or just watch a planet spiral into a star, Orbit-Sandbox provides an honest physics engine that behaves like the real universe.

## Current Features

- 🪐 **Real-world planetary simulations:**
  - Six planets available: Mercury, Venus, Earth, Mars, Jupiter, Saturn
  - Accurate orbital parameters (semi-major axis, period, mass)
  - Real astronomical units (AU, solar masses, years)
  - Three orbital scenarios: circular, elliptical, escape trajectory
- ⚙️ **Honest physics simulation:**
  - Newtonian gravity (inverse square law)
  - Semi-implicit Euler integration
  - Conserves angular momentum
  - No hardcoded orbital paths
  - Proper G constant calculated for AU/year system
- 🎮 **Interactive visualization (1280×720 window):**
  - Real-time Pygame rendering at 60 FPS
  - Mouse wheel zoom (50-2000 pixels per AU)
  - Toggleable orbital trail rendering (T key)
  - Toggleable grid overlay (G key)
  - Static starfield background
  - Pause/resume with spacebar
  - Adjustable simulation speed (UP/DOWN arrows)
  - Reset simulation with R key
  - ESC to return to menu
- 📊 **Comprehensive HUD display:**
  - Real-time FPS counter
  - Zoom level indicator
  - Simulation speed multiplier
  - Elapsed simulation time (years) and real time (seconds)
  - Distance from star (AU and km)
  - Orbital velocity (AU/yr and km/s)
- 🖥️ **Console mode:**
  - CLI planet and scenario selection
  - Periodic position/distance/velocity output
  - Ctrl+C graceful exit
- 📊 **Data export:**
  - CSV logging for post-simulation analysis
  - Matplotlib plotting script included
- 🎯 **Modular architecture:**
  - Clean package structure (orbit/, ui/, tools/)
  - Easy to extend with new planets or scenarios
  - Separation between physics engine and visualization

## Project Structure

The codebase is organized with clear separation of concerns:

```
Orbit-Sandbox/
├── main.py            # Entry point - CLI argument handling
├── orbit/             # Core simulation engine
│   ├── body.py        # Body class - position, velocity, mass
│   ├── physics.py     # Gravity calculations and orbital velocity formulas
│   ├── simulation.py  # Simulation class - physics loop and time stepping
│   ├── systems.py     # Scenario factory functions (circular, elliptical, escape)
│   ├── units.py       # Real-world unit conversions (AU, solar masses, years)
│   └── planets.py     # Real planet data (Mercury, Venus, Earth, Mars, Jupiter, Saturn)
├── ui/                # Visualization layer
│   └── visualize.py   # Pygame rendering, HUD, and interactive controls
├── tools/             # Analysis utilities
│   └── plot_orbit.py  # Matplotlib plotting script for CSV data
└── requirements.txt   # Python dependencies
```

Core classes:
- **Body:** Represents a physical object with position, velocity, and mass
- **Simulation:** Orchestrates the physics loop and advances time in AU/year units
- **Visualization:** Handles Pygame rendering, HUD, menu, and user input

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

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Console Mode

Run a specific scenario with terminal output:

```bash
# Circular orbit with Earth (default)
python main.py --scenario circular

# Choose a different planet
python main.py --scenario circular --planet mars
python main.py --scenario circular --planet jupiter

# Elliptical orbit
python main.py --scenario elliptical --planet earth

# Escape trajectory
python main.py --scenario escape --planet venus
```

Available planets: `mercury`, `venus`, `earth`, `mars`, `jupiter`, `saturn` (case-insensitive)

Output shows time, position, distance from star, and orbital speed at regular intervals.

### Visualization Mode

#### With menu selection:
```bash
# Visualize Earth orbit (default)
python main.py --visualize

# Choose a different planet
python main.py --visualize --planet mars
python main.py --visualize --planet jupiter
```
This opens a menu where you can click to choose a scenario.

#### Direct to a specific scenario:
```bash
python main.py --visualize --scenario circular --planet earth
python main.py --visualize --scenario circular --planet saturn
```

**Visualization Controls:**
- **Mouse wheel / +/- keys:** Zoom in/out (50x to 2000x)
- **Spacebar:** Pause/resume simulation
- **UP/DOWN arrows:** Adjust simulation speed (0.1x to 10x+)
- **R:** Reset simulation to initial conditions
- **G:** Toggle grid overlay
- **T:** Toggle orbital trail
- **ESC:** Return to scenario menu

### Data Export and Plotting

Generate CSV data from a simulation run (requires minor code modification to use `sim.run_and_log()` instead of `sim.run_continuous()`), then plot the results:

```bash
python plot_orbit.py
```

This creates a 4-panel plot showing:
- Orbital path (x vs y)
- Distance from star over time
- Orbital speed over time
- Phase space diagram (distance vs speed)

## Requirements

- **Python 3.12 or 3.13** (Python 3.14 not yet supported due to pygame compatibility issues)
- NumPy
- Pygame
- Matplotlib (optional - for plotting)
- Pandas (optional - for plotting)

## How it Works

### Physics Engine

The simulation uses Newton's law of universal gravitation:

```
F = G * m1 * m2 / r²
```

Acceleration is computed from force, then semi-implicit Euler integration updates velocity and position:

```python
velocity += acceleration * dt  # Update velocity first
position += velocity * dt       # Then update position
```

This ordering (velocity before position) gives much better energy conservation than naive Euler integration, keeping orbits stable over long timescales.

### Numerical Integration

The simulator uses a fixed timestep (`dt = 0.001 years`) and advances the universe forward in discrete steps. Each step:
1. Computes gravitational acceleration based on current positions
2. Updates velocities using acceleration
3. Updates positions using new velocities
4. Advances simulation time

This is an approximation of continuous calculus with small rectangles - the smaller the timestep, the more accurate the simulation.

### Real-World Units

The simulation uses astronomical units for realistic scale:
- **Distance:** Astronomical Units (AU) - 1 AU = Earth-Sun distance ≈ 149.6 million km
- **Mass:** Solar masses (M☉) - 1 M☉ = mass of the Sun
- **Time:** Years - 1 year = Earth orbital period
- **Gravitational constant:** G = 39.478 AU³/(M☉·year²)

At the default simulation speed (1×), 1 complete Earth orbit takes 10 real-world seconds.

## Known Limitations & Future Work

**Current limitations:**
- Single central mass only (star doesn't move)
- 2D simulation (no z-axis)
- Semi-implicit Euler integration (good but not perfect)
- Only inner planets and gas giants (no ice giants yet)

**Planned features:**
- N-body physics (multiple bodies affecting each other)
- Multiple integration methods (Verlet, RK4)
- Binary star systems
- 3-body chaos demonstrations (figure-8 orbits)
- Lagrange point demonstrations
- Energy/momentum conservation tracking
- Velocity and acceleration vector visualizations
- Orbital prediction mode (dotted path showing future trajectory)
- More planets (Uranus, Neptune, dwarf planets)
- Click to place custom bodies
- Adjustable gravitational constant for experiments
- Customizable trail length and colors

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
