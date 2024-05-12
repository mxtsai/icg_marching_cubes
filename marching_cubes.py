"""
This is an implementation of the Marching Cubes algorithm without interpolation.
I assume points in the object as '1' and points outside the object as -1.
This is a simple implementation of the algorithm, and it doesn't include interpolation.
"""

import numpy as np

from stl import mesh
from mc_lookup_table import get_edges, edge_idx_to_unit_square_mapping

############### MARCHING CUBES IMPLEMENTATION ###############
#        Vertex Layout                  Edge Layout
#
#         6             7
#         +-------------+               +-----6-------+   
#       / |           / |             / |            /|   
#     /   |         /   |          11   7         10   5
# 2 +-----+-------+  3  |         +-----+2------+     |   
#   |   4 +-------+-----+ 5       |     +-----4-+-----+   
#   |   /         |   /           3   8         1   9
#   | /           | /             | /           | /       
# 0 +-------------+ 1             +------0------+         


# Coordinate System:
#
#              (0,1,-1)               (1,1,-1)
#                +-------------------+
#               /|                  /|
#              / |                 / |   
#             /  |                /  |
#            /   |               /   |     
#    (0,1,0)+-------------------+(1,1,0)
#           |    | (0,0,-1)     |    |
#           |    +--------------|--- + (1,0,-1)
#           |   /               |   /
#           |  /                |  /
#           | /                 | /
#           |/                  |/
#    (0,0,0)+-------------------+(1,0,0)
#
#
#           z
#           ^  
#           | /y
#           |/
#           +------> x

    
def apply_translation(triangle, delta_x, delta_y, delta_z):
    return [(x + delta_x, y + delta_y, z + delta_z) for x, y, z in triangle]
    
def marching_cubes_naive(voxel):

    output_dim = np.array(voxel.shape) - 1      # compute the output dimension

    vector_list = []

    # assume i, j, k
    for i in range(output_dim[0]):
        for j in range(output_dim[1]):
            for k in range(output_dim[2]):

                # compute the edge encoding
                # follow the order of the vertex layout above
                binary_0 = int(voxel[i+1][j][k] > 0)
                binary_1 = int(voxel[i+1][j+1][k] > 0)
                binary_2 = int(voxel[i][j][k] > 0)
                binary_3 = int(voxel[i][j+1][k] > 0)
                binary_4 = int(voxel[i+1][j][k+1] > 0)
                binary_5 = int(voxel[i+1][j+1][k+1] > 0)
                binary_6 = int(voxel[i][j][k+1] > 0)
                binary_7 = int(voxel[i][j+1][k+1] > 0)

                bit_encoding = [binary_7, binary_6, binary_5, binary_4, binary_3, binary_2, binary_1, binary_0]
                
                # convert to number
                lookup_idx = np.packbits(bit_encoding)[0]
                edges = get_edges(lookup_idx)

                if len(edges) == 0:
                    continue    # no triangles to build
                
                # build triangles from edges

                # convert edge index to unit square mapping
                unit_square_coordinates = [[edge_idx_to_unit_square_mapping(e) for e in e_list] for e_list in edges]

                # apply translation
                delta_x = j
                delta_y = output_dim[0] - i
                delta_z = -k
                translated_coordinates = [apply_translation(triangle, delta_x, delta_y, delta_z) for triangle in unit_square_coordinates]

                # add to vector list
                vector_list.extend(translated_coordinates)

    final_mesh = mesh.Mesh(np.zeros(len(vector_list), dtype=mesh.Mesh.dtype))
    for triangle_i, triangle in enumerate(vector_list):
        final_mesh.vectors[triangle_i][:] = np.array(triangle)

    return final_mesh


if __name__ == "__main__":

    from myplot import plot_mesh
    from load_voxels import *

    example = create_multiple_objects()
    cubes = marching_cubes_naive(example)

    # to plot the mesh (suggested for mesh under 64x64x64)
    plot_mesh(cubes)

    # # save to stl (suggested for mesh larger than 64x64x64)
    # cubes.save('cube.stl')