# This script reads an h5 file and save x and y data for each node to a CSV file.

import h5py
import numpy as np
import pandas as pd

# Open the file
filename = 'finch_8458_aktiv.analysis.h5'

# Use the h5py library to open the file
with h5py.File(filename, "r") as f:
    dset_names = list(f.keys())
    locations = f["tracks"][:].T
    node_names = [n.decode() for n in f["node_names"][:]]

print("===filename===")
print(filename)
print()

frame_count, node_count, _, instance_count = locations.shape
print("frame count:", frame_count)
print("node count:", node_count)
print("instance count:", instance_count)
print()

print("===HDF5 datasets===")
print(dset_names)
print()

print("===locations data shape===")
print(locations.shape)
print()

# Create an empty pandas DataFrame to store x and y data
df = pd.DataFrame()

print("===nodes===")
for i, name in enumerate(node_names):
    print(f"{i}: {name}")
    # Access the data from this node in the locations array and store it in a variable called data
    data = locations[:, i, :, 0]
    x = data[:,0]
    y = data[:,1]
    print(x)
    print(y)
    # Convert the data to a pandas DataFrame
    df[name + "_x"] = x
    df[name + "_y"] = y

# Export the data to a CSV file
df.to_csv(filename[:-3] + ".csv", index=False)

# Convert index to column at position 0
df.reset_index(level=0, inplace=True)

# Rename the index column to "frame"
df.rename(columns={"index": "frame"}, inplace=True)

# Drop nan values
df = df.dropna()

# Export the data to a CSV file
df.to_csv(filename[:-3] + "_dropnan.csv", index=False)
