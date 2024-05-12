import numpy as np

def create_sphere_voxels(space_val=-1, object_val=1):
    voxels = space_val*np.ones((128, 128, 128))
    center = np.array([50, 50, 50])
    radius = 30

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