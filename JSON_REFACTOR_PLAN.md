# JSON Refactor - Quick Reference 📋

## Goal
Move from hardcoded `systems.py` to JSON-based system definitions **before** implementing N-body physics.

---

## What We're Building

### 1. Data Structure
```
data/
├── bodies.json          # Library of reusable bodies (Sun, Earth, Jupiter, etc.)
└── systems/
    ├── circular.json
    ├── elliptical.json
    └── escape.json
```

### 2. JSON Format Examples

**data/bodies.json** - Body library:
```json
{
  "sun": {"mass": 1.0, "radius": 10, "color": [255, 255, 0]},
  "earth": {"mass": 3.0e-6, "radius": 4, "color": [100, 150, 255]},
  "jupiter": {"mass": 9.5e-4, "radius": 8, "color": [200, 150, 100]}
}
```

**data/systems/circular.json** - Complete system:
```json
{
  "name": "Circular Orbit",
  "bodies": [
    {
      "template": "sun",
      "position": [0.0, 0.0],
      "velocity": [0.0, 0.0]
    },
    {
      "template": "earth",
      "position": [1.0, 0.0],
      "velocity": [0.0, 6.28]
    }
  ]
}
```

### 3. New Code: orbit/loader.py
```python
class SystemLoader:
    def load_system(filepath) -> List[Body]
    def save_system(bodies, filepath)
    def _load_bodies_library()
```

### 4. Update main.py
```python
# New way (JSON)
loader = SystemLoader()
bodies = loader.load_system('data/systems/circular.json')

# Old way (backward compatible)
bodies, G = create_simple_system(PLANETS['earth'])
```

---

## Implementation Steps

1. Design JSON format
2. Create data/ directory + example files
3. Implement SystemLoader class
4. Update main.py to support --config flag
5. Convert existing 3 scenarios to JSON
6. Test visualization + console modes
7. Deprecate orbit/systems.py (keep for compatibility)
8. **THEN** start N-body implementation

---

## Why This Matters

- Clean data/code separation
- User-shareable system files
- JSON naturally supports N bodies (not just 2)
- Both visualization + console use same files
- Foundation for future UI system builder

---

## Timeline

**Before N-body:** JSON refactor (1-2 sessions)  
**After refactor:** N-body physics (3-4 sessions)  
**Much later:** In-app system builder UI

---

## Current Status
- **Planning phase** - not implemented yet
- Next step: Create JSON format + example files
- Keep console mode - just make it load JSON

---

## Key Notes from orbit/systems.py

Current scenarios to convert:
- create_simple_system() → circular.json (100% circular velocity)
- create_elliptical_orbit() → elliptical.json (70% circular velocity)
- create_escape_trajectory() → escape.json (120% escape velocity)

All use same planet data from PLANETS dict (semi_major_axis, mass).
All create star at origin + planet at orbital radius on x-axis, velocity in +y.
