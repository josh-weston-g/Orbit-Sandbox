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
    def list_systems(directory='data/systems'):
        """
        List available system JSON files in a directory.
        
        param: directory: path to directory containing JSON files

        returns: list of tuples: (filename_without_extension, full_path)
        """
        systems = []
        if os.path.exists(directory):
            for filename in os.listdir(directory):
                if filename.endswith('.json'):
                    name = filename[:-5]  # Remove .json extension
                    full_path = os.path.join(directory, filename)
                    systems.append((name, full_path))
        return sorted(systems)