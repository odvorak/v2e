import subprocess
import os
from pathlib import Path

# Define the path to v2e.py
v2e_path = "v2e.py"

# Get the root directory containing subfolders
root_dir = Path("E:\\EBAL_v10\\train\\")  # Change this to your actual root directory

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
                "--avi_frame_rate": "40",  # AVI_FRAME_RATE
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
