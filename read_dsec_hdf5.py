import h5py


def read_hdf5(file_path):
    with h5py.File(file_path, 'r') as f:
        # Read t_offset
        t_offset = f['t_offset'][()]  # Extract the scalar value
        print(f"t_offset: {t_offset}")

        # Read event data
        x_data = f['events/x'][:50]
        y_data = f['events/y'][:50]
        p_data = f['events/p'][:50]
        t_data = f['events/t'][:50]
        ms_to_idx = f['ms_to_idx'][:50]

        # Print first 50 events
        print("First 50 events:")
        for i in range(50):
            print(f"t: {t_data[i]}, x: {x_data[i]}, y: {y_data[i]}, p: {p_data[i]}, ms_to_idx: {ms_to_idx[i]}")

# Example usage
read_hdf5("E:\\EBAL_v10\\train\\D3\\events.h5")