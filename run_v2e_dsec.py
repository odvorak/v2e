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


# Define the path to v2e.py
v2e_path = "v2e.py"

# Get the root directory containing subfolders
#root_dir = Path("/root/train")
root_dir= Path("/root/train_20_videos/")

# Iterate through all subfolders
for subfolder in root_dir.iterdir():
    if subfolder.is_dir():
        flight_mp4 = subfolder / "flight.mp4"
        events_h5 = subfolder / "events.h5"

        if flight_mp4.exists():
            print(f"Processing: {flight_mp4}")

            # Define options
            options = {
                "-o": str(subfolder),  # Save output in the same folder
                "--dvs_h5": str(events_h5),  # Output events.h5 file
                "--output_in_place": "",  # OUTPUT_IN_PLACE
                "--overwrite": True,  # OVERWRITE
                "--unique_output_folder": "",  # UNIQUE_OUTPUT_FOLDER
                "--skip_video_output": True,  # SKIP_VIDEO_OUTPUT
                "--auto_timestamp_resolution": "",  # AUTO_TIMESTAMP_RESOLUTION
                "--timestamp_resolution": "",  # TIMESTAMP_RESOLUTION
                "--dvs_params": "",  # DVS_PARAMS
                "--pos_thres": "0.7",  # POS_THRES
                "--neg_thres": "0.7",  # NEG_THRES
                "--sigma_thres": "0.03",  # SIGMA_THRES
                "--cutoff_hz": "200",  # CUTOFF_HZ
                "--leak_rate_hz": "0",  # LEAK_RATE_HZ
                "--shot_noise_rate_hz": "",  # SHOT_NOISE_RATE_HZ
                "--photoreceptor_noise": False,  # PHOTORECEPTOR_NOISE
                "--leak_jitter_fraction": "",  # LEAK_JITTER_FRACTION
                "--noise_rate_cov_decades": "",  # NOISE_RATE_COV_DECADES
                "--refractory_period": "",  # REFRACTORY_PERIOD
                "--dvs_emulator_seed": "",  # DVS_EMULATOR_SEED
                "--show_dvs_model_state": "",  # SHOW_DVS_MODEL_STATE
                "--save_dvs_model_state": False,  # SAVE_DVS_MODEL_STATE
                "--record_single_pixel_states": False,  # RECORD_SINGLE_PIXEL_STATES
                "--output_height": "200",  # OUTPUT_HEIGHT
                "--output_width": "200",  # OUTPUT_WIDTH
                "--dvs128": False,  # DVS128
                "--dvs240": False,  # DVS240
                "--dvs346": False,  # DVS346
                "--dvs640": False,  # DVS640
                "--dvs1024": False,  # DVS1024
                "--disable_slomo": True,  # DISABLE_SLOMO
                "--slomo_model": "",  # SLOMO_MODEL
                "--batch_size": "8",  # BATCH_SIZE
                "--vid_orig": "",  # VID_ORIG
                "--vid_slomo": "",  # VID_SLOMO    "--start_time": "",  # START_TIME

                "--slomo_stats_plot": False,  # SLOMO_STATS_PLOT
                "-i": str(flight_mp4),  # Input video
                "--input_frame_rate": "1000",  # INPUT_FRAME_RATE
                "--input_slowmotion_factor": "",  # INPUT_SLOWMOTION_FACTOR
                "--stop_time": "",  # STOP_TIME
                "--crop": "",  # CROP
                "--hdr": False,  # HDR
                "--synthetic_input": "",  # SYNTHETIC_INPUT
                # "--dvs_exposure": "",  # DVS_EXPOSURE
                "--dvs_vid": "",  # DVS_VID
                "--dvs_vid_full_scale": "",  # DVS_VID_FULL_SCALE
                "--no_preview": False,  # NO_PREVIEW
                "--ddd_output": False,  # DDD_OUTPUT
                "--dvs_aedat2": "",  # DVS_AEDAT2
                "--dvs_text": "",  # DVS_TEXT
                "--label_signal_noise": False,  # LABEL_SIGNAL_NOISE
                "--cs_lambda_pixels": "",  # CS_LAMBDA_PIXELS
                "--cs_tau_p_ms": "",  # CS_TAU_P_MS
                "--scidvs": False,  # SCIDVS
            }

            # Construct command
            cmd = ["python", v2e_path]
            for opt, val in options.items():
                if isinstance(val, bool):
                    if val:
                        cmd.append(opt)
                elif val != "":
                    cmd.append(opt)
                    cmd.append(val)

            # Run the command
            print("Running:", " ".join(cmd))
            try:
                subprocess.run(cmd, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error processing {flight_mp4}: {e}")

            hdf5_to_dsec(str(events_h5))

