import subprocess
import os
from pathlib import Path
import h5py
import numpy as np


def generate_ms_to_idx(timestamps):
    """
    Generates the ms_to_idx array based on the event timestamps.

    Args:
        timestamps (np.ndarray): Array of event timestamps in microseconds.

    Returns:
        ms_to_idx (np.ndarray): Array mapping milliseconds to event indices.
    """
    max_ms = (timestamps[-1] // 1000) + 1  # Calculate the number of milliseconds covered by the timestamps

    ms_to_idx = np.zeros(max_ms - 1, dtype=np.int64)  # Initialize the ms_to_idx array

    current_idx = 0

    for ms in range(1, max_ms):
        while (current_idx) < len(timestamps) and timestamps[current_idx] < ms * 1000:
            current_idx += 1
        ms_to_idx[ms - 1] = current_idx
    return ms_to_idx


def hdf5_to_dsec(file_path):
    # Open the file in read/write mode
    with h5py.File(file_path, 'r+') as f:
        events = f['events']
        t = events[:, 0]  # Time
        x = events[:, 1]  # X coordinate
        y = events[:, 2]  # Y coordinate
        p = events[:, 3]  # Polarity
        # Extract and adjust timestamps
        ms_to_idx = generate_ms_to_idx(t)

        # Remove existing datasets if they exist
        for key in ['events']:
            if key in f:
                del f[key]

        # Create new datasets
        f.create_dataset('events/t', data=t)
        f.create_dataset('events/x', data=x)
        f.create_dataset('events/y', data=y)
        f.create_dataset('events/p', data=p)
        f.create_dataset('ms_to_idx', data=ms_to_idx)
        f.create_dataset('t_offset', data=0)

import subprocess
import os
from pathlib import Path

# Define the path to v2e.py
v2e_path = "v2e.py"

# Get the root directory containing subfolders
root_dir = Path("E:\\EBAL_v10\\test\\")  # Change this to your actual root directory

# Iterate through all subfolders
for subfolder in root_dir.iterdir():
    if subfolder.is_dir():
        print("Processing subfolder: ", subfolder)
        events_h5 = subfolder / "events.h5"
        hdf5_to_dsec(events_h5)
