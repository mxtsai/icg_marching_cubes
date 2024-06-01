import os
import numpy as np
import cv2

def create_sphere_voxels(space_val=-1, object_val=1):
    voxels = space_val*np.ones((40, 40, 40))
    center = np.array([20, 20, 20])
    radius = 5

    for i in range(voxels.shape[0]):
        for j in range(voxels.shape[1]):
            for k in range(voxels.shape[2]):
                distance = np.linalg.norm(np.array([i, j, k]) - center)
                if distance <= radius:
                    voxels[i, j, k] = object_val

    return voxels

def create_multiple_objects(space_val=-1, object_val=1):
    space = space_val*np.ones((64, 64, 64))
    
    space[10:20, 10:30, 10:20] = object_val

    center1 = np.array([40, 40, 40])
    radius1 = 5
    for i in range(space.shape[0]):
        for j in range(space.shape[1]):
            for k in range(space.shape[2]):
                distance1 = np.linalg.norm(np.array([i, j, k]) - center1)
                if distance1 <= radius1:
                    space[i, j, k] = object_val
    center2 = np.array([50, 50, 20])
    radius2 = 7
    for i in range(space.shape[0]):
        for j in range(space.shape[1]):
            for k in range(space.shape[2]):
                distance2 = np.linalg.norm(np.array([i, j, k]) - center2)
                if distance2 <= radius2:
                    space[i, j, k] = object_val
    return space

def create_dummy_voxels(space_val=-1, object_val=1):

    space = space_val*np.ones((4, 4, 4))
    space[1:3, 1:3, 1:3] = object_val

    return space

def load_ct_folder(folder_dir):

    # get all the files in the folder
    files = sorted(os.listdir(folder_dir))

    height, width, depth = None, None, len(files)

    # read the first file to get the dimensions
    img = cv2.imread(os.path.join(folder_dir, files[0]), cv2.IMREAD_GRAYSCALE)
    height, width = img.shape

    # create the numpy array
    numpy_file = np.zeros((height, width, depth))

    # read all the files
    for i, file in enumerate(files):
        img = cv2.imread(os.path.join(folder_dir, file), cv2.IMREAD_GRAYSCALE)
        numpy_file[:, :, i] = img

    print(f"Loaded {depth} images from {folder_dir}")
    print(f"Dimensions: {numpy_file.shape}")
    print(f"Max value: {numpy_file.max()}")
    print(f"Min value: {numpy_file.min()}")
    print(f"Mean value: {numpy_file.mean()}")
    print(f"Median value: {np.median(numpy_file)}")
    
    return numpy_file

def load_ct_folder_gaps(folder_dir, gaps=1):
    # get all the files in the folder
    files = sorted(os.listdir(folder_dir))

    height, width, depth = None, None, len(files) + (len(files) - 1) * gaps

    # read the first file to get the dimensions
    img = cv2.imread(os.path.join(folder_dir, files[0]), cv2.IMREAD_GRAYSCALE)
    height, width = img.shape

    # create the numpy array
    numpy_file = np.zeros((height, width, depth))

    # read all the files
    for i, file in enumerate(files):
        img = cv2.imread(os.path.join(folder_dir, file), cv2.IMREAD_GRAYSCALE)
        numpy_file[:, :, gaps*i] = img
    
    # interpolate the gaps
    if gaps > 1:
        for i in range(1, len(files)):
            for gap in range(1, gaps):
                numpy_file[:, :, gaps*i + gap] = (numpy_file[:, :, gaps*i] * (gaps - gap) + numpy_file[:, :, gaps*(i+1)] * gap) / gaps
                
    print(f"Loaded {len(files)} images from {folder_dir}, filling gaps with {gaps} images")
    print(f"Dimensions: {numpy_file.shape}")
    print(f"Max value: {numpy_file.max()}")
    print(f"Min value: {numpy_file.min()}")
    print(f"Mean value: {numpy_file.mean()}")
    print(f"Median value: {np.median(numpy_file)}")

    return numpy_file