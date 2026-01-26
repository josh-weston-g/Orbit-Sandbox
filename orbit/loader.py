"""
System loader for JSON-based orbital system definitions.
"""

import json
import os
from .body import Body
from .units import G_AU

class SystemLoader:
    """Load orbital systems from JSON files."""

    @staticmethod
    def load_from_dict(data):
        """
        Load a system from a dictionary (parsed JSON).

        param: data: dict containing system definition

        returns: tupple: (bodies, G, metadate)
        """
        # Extract metadata
        metadata = {
            'name': data.get('name', 'Unnamed System'),
            'description': data.get('description', ''),
        }

        # Get gravitational constant (default to G_AU if not specified)
        G = data.get('G', G_AU)

        # Create bodies
        bodies = []
        for body_data in data['bodies']:
            body = Body(
                position=body_data['position'],
                velocity=body_data['velocity'],
                mass=body_data['mass'],
                name=body_data.get('name'),   # Optional name
                body_type=body_data.get('type', 'body')   # Optional type
            )
            bodies.append(body)

        return bodies, G, metadata
    
    @staticmethod
    def load_from_file(filepath):
        """
        Load a system from a JSON file.
        
        param: filepath: path to JSON file
        
        returns: tupple: (bodies, G, metadate)
        """
        with open(filepath, 'r') as f:
            data = json.load(f)

        return SystemLoader.load_from_dict(data)
    
    @staticmethod
    def list_systems():
        """
        List available system JSON files in a directory.

        returns: dict: { 'default': [(name, path), ...], 
                        'custom': [(name, path), ...]}
        """
        import os

        default_dir = 'data/default_systems'
        custom_dir = 'data/custom_systems'

        default_systems = []
        custom_systems = []

        # Get default systems
        if os.path.exists(default_dir):
            for filename in os.listdir(default_dir):
                if filename.endswith('.json'):
                    name = filename[:-5]  # Remove .json extension
                    path = os.path.join(default_dir, filename)
                    default_systems.append((name, path))

        # Get custom systems
        if os.path.exists(custom_dir):
            for filename in os.listdir(custom_dir):
                if filename.endswith('.json'):
                    name = filename[:-5]  # Remove .json extension
                    path = os.path.join(custom_dir, filename)
                    custom_systems.append((name, path))

        return {
            'default': sorted(default_systems),
            'custom': sorted(custom_systems)
        }