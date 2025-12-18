import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV file
df = pd.read_csv('orbit_data.csv')

# Create a figure with multiple subplots
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# 1. Orbital path (x vs y position)
axes[0, 0].plot(df['x'], df['y'], 'b-', linewidth=0.5, alpha=0.7)
axes[0, 0].plot(df['x'].iloc[0], df['y'].iloc[0], 'go', markersize=10, label='Start')
axes[0, 0].plot(df['x'].iloc[-1], df['y'].iloc[-1], 'ro', markersize=10, label='End')
axes[0, 0].plot(0, 0, 'y*', markersize=15, label='Central Body')
axes[0, 0].set_xlabel('X Position')
axes[0, 0].set_ylabel('Y Position')
axes[0, 0].set_title('Orbital Path')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)
axes[0, 0].axis('equal')

# 2. Distance from center over time
axes[0, 1].plot(df['time'], df['distance'], 'r-', linewidth=1)
axes[0, 1].set_xlabel('Time')
axes[0, 1].set_ylabel('Distance from Center')
axes[0, 1].set_title('Distance vs Time')
axes[0, 1].grid(True, alpha=0.3)

# 3. Speed over time
axes[1, 0].plot(df['time'], df['speed'], 'g-', linewidth=1)
axes[1, 0].set_xlabel('Time')
axes[1, 0].set_ylabel('Speed')
axes[1, 0].set_title('Speed vs Time')
axes[1, 0].grid(True, alpha=0.3)

# 4. Velocity components over time
axes[1, 1].plot(df['time'], df['vx'], 'b-', linewidth=1, label='vx', alpha=0.7)
axes[1, 1].plot(df['time'], df['vy'], 'r-', linewidth=1, label='vy', alpha=0.7)
axes[1, 1].set_xlabel('Time')
axes[1, 1].set_ylabel('Velocity')
axes[1, 1].set_title('Velocity Components vs Time')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
# plt.savefig('orbit_visualization.png', dpi=300, bbox_inches='tight')
plt.show()

# Print some statistics
print("\n=== Orbit Statistics ===")
print(f"Total simulation time: {df['time'].iloc[-1]:.2f}")
print(f"Number of steps: {len(df)}")
print(f"Initial distance: {df['distance'].iloc[0]:.2f}")
print(f"Final distance: {df['distance'].iloc[-1]:.2f}")
print(f"Min distance: {df['distance'].min():.2f}")
print(f"Max distance: {df['distance'].max():.2f}")
print(f"Initial speed: {df['speed'].iloc[0]:.4f}")
print(f"Final speed: {df['speed'].iloc[-1]:.4f}")
print(f"Average speed: {df['speed'].mean():.4f}")