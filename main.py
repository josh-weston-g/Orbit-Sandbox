"""
Orbit-Sandbox - N-body gravitational simulation with interactive visualization.

Usage:
    python main.py [--resolution RESOLUTION]

Options:
    --resolution    Window resolution: auto, 720p, 1080p, 1440p (default: auto)
"""

import argparse
from ui.visualize import run_visualization

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Orbit-Sandbox - Interactive N-body orbital mechanics simulator"
    )
    parser.add_argument(
        '--resolution',
        type=str,
        default='auto',
        choices=['auto', '720p', '1080p', '1440p'],
        help='Window resolution (default: auto - fullscreen borderless)'
    )
    
    args = parser.parse_args()
    
    # Launch visualization with menu
    run_visualization(resolution=args.resolution)