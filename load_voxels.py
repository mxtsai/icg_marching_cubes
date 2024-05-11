import numpy as np

def create_sphere_voxels():
        
        voxels = np.zeros((128, 128, 128))
        center = np.array([50, 50, 50])
        radius = 30

        for i in range(voxels.shape[0]):
            for j in range(voxels.shape[1]):
                for k in range(voxels.shape[2]):
                    distance = np.linalg.norm(np.array([i, j, k]) - center)
                    if distance <= radius:
                        voxels[i, j, k] = 1

        return voxels

def create_multiple_objects():
    space = np.zeros((32, 32, 32))
    
    # Create first sphere
    center1 = np.array([20, 20, 20])
    radius1 = 3
    for i in range(32):
        for j in range(32):
            for k in range(32):
                distance1 = np.linalg.norm(np.array([i, j, k]) - center1)
                if distance1 <= radius1:
                    space[i, j, k] = 1
    
    # Create second sphere
    center2 = np.array([5, 5, 5])
    radius2 = 2
    for i in range(32):
        for j in range(32):
            for k in range(32):
                distance2 = np.linalg.norm(np.array([i, j, k]) - center2)
                if distance2 <= radius2:
                    space[i, j, k] = 1
    
    # Create rectangle
    for i in range(10, 20):
        for j in range(5, 15):
            for k in range(10, 20):
                space[i, j, k] = 1
    
    return space

def create_dummy_voxels():

    # a dummpy voxel for now
    voxels = np.zeros((4, 4, 4))
    voxels[1:3, 1:3, 1:3] = 1

    return voxels