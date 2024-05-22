"""
This is an implementation of the Marching Tetrahedra algorithm with interpolation.
"""

import numpy as np

from stl import mesh
from tetrahedra_lookup_table import edge_to_vertex, \
    edge_idx_to_unit_tetrahedra_mapping, binary_to_base10, get_edge

def inverse_linear_interpolation(threshold, v1, v2):
    return (threshold - v1)/(v2 - v1)

def process_cubic_voxel(voxel, threshold):
    """process the 2x2x2 (cubic) voxel"""

    # each cubic voxel consists of 6 tetrahedrons
    cube_tetra_vertices = [
        [0, 2, 3, 7],
        [0, 1, 3, 7],
        [0, 1, 5, 7],
        [0, 2, 6, 7],
        [0, 4, 6, 7],
        [0, 4, 5, 7]
    ]

    # process each tetrahedra
    face_coordinates = []

    for tetra_i, t_vertices in enumerate(cube_tetra_vertices):

        # get values of tetrahedra
        tetra_values = voxel[t_vertices]

        # get bit encoding (end up with v3, v2, v1, 0)
        bit_encoding = (tetra_values > threshold).astype(int)[::-1]

        # compute lookup index
        lookup_idx = binary_to_base10(bit_encoding)

        # get edges
        edges_triplets = get_edge(lookup_idx)    # list of triplets

        # process trianges
        for edge_set in edges_triplets:
            triangle_coordinates = []
            for edge in edge_set:

                # compute the start and end point
                start_vertex_idx, end_vertex_idx = edge_to_vertex(edge)

                # get the values of the start and end vertex points
                start_val = tetra_values[start_vertex_idx]
                end_val = tetra_values[end_vertex_idx]

                # subtract by the threshold (to enable crossing)
                # start_val -= threshold
                # end_val -= threshold

                # compute the interpolated point
                # alpha = start_val/(start_val - end_val)
                # alpha = 0.5
                alpha = inverse_linear_interpolation(threshold, start_val, end_val)
                # print(f"Edge: {edge} - Alpha: {alpha} - TetraID: {tetra_i}")

                edge_coordinates = edge_idx_to_unit_tetrahedra_mapping(edge, tetra_i, alpha=alpha)
                triangle_coordinates.append(edge_coordinates)
            face_coordinates.append(triangle_coordinates)
        
    return face_coordinates

def apply_translation(triangle, delta_x, delta_y, delta_z):
    return [(x + delta_x, y + delta_y, z + delta_z) for x, y, z in triangle]

def marching_tetrahedra(voxel, threshold=0.0):

    output_dim = np.array(voxel.shape) - 1      # compute the output dimension

    vector_list = []

    # iterate through the voxel grid
    for i in range(output_dim[0]):
        for j in range(output_dim[1]):
            for k in range(output_dim[2]):

                # follow ordering from 0 to 7 of the vertex layout (use same as Marching Cubes)
                neighbors = np.array([voxel[i+1][j][k], voxel[i+1][j+1][k], voxel[i][j][k], voxel[i][j+1][k],
                                voxel[i+1][j][k+1], voxel[i+1][j+1][k+1], voxel[i][j][k+1], voxel[i][j+1][k+1]])
                
                # process each cubic voxel
                unit_tetra_coordinates = process_cubic_voxel(neighbors, threshold)

                # translate
                delta_x = j
                delta_y = k
                delta_z = output_dim[0] - i - 1
                translated_coordinates = [apply_translation(triangle, delta_x, delta_y, delta_z) for triangle in unit_tetra_coordinates]

                # add to vector list
                vector_list.extend(translated_coordinates)

                # final_mesh = mesh.Mesh(np.zeros(len(vector_list), dtype=mesh.Mesh.dtype))
                # for triangle_i, triangle in enumerate(vector_list):
                #     final_mesh.vectors[triangle_i][:] = np.array(triangle)

                # print(i, j, k)
                # print(translated_coordinates)
                # plot_mesh(final_mesh)
    
    final_mesh = mesh.Mesh(np.zeros(len(vector_list), dtype=mesh.Mesh.dtype))
    for triangle_i, triangle in enumerate(vector_list):
        final_mesh.vectors[triangle_i][:] = np.array(triangle)

    return final_mesh

if __name__ == "__main__":

    from myplot import plot_mesh
    from load_voxels import *
    import time

    # create a simple 2x2x2 voxel grid
    # example = np.ones((2, 2, 2))*-1
    # example[0, 0 ,0] = 1    # ok
    # example[1, 0, 0] = 1    # not ok
    # example[0, 1, 0] = 1    # oks
    # example[0, 0, 1] = 1    # ok
    # example[1, 1, 0] = 1    # ok
    # example[1, 0, 1] = 1    # ok
    # example[0, 1, 1] = 1    # not ok
    # example[1, 1, 1] = 1    # ok

    # print(example)
    # example = create_sphere_voxels()

    # example = np.ones((3, 3, 3))*-1
    # example[1, 1, 1] = 1

    example = create_multiple_objects()
    
    tetra_mesh = marching_tetrahedra(example, threshold=0)

    # to plot the mesh (suggested for mesh under 64x64x64)
    # plot_mesh(tetra_mesh)

    tetra_mesh.save("tetrahedra.stl")

