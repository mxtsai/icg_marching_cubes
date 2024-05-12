import numpy as np

from stl import mesh
from mc_lookup_table import get_edges
from myplot import plot_mesh

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

def edge_idx_to_unit_square_mapping(edge_idx):
    "maps the edge index to a unit square coordinate"

    assert edge_idx in list(range(12)), f"{edge_idx} out of range 0-11"

    if edge_idx == 0:
        return (0.5, 0, 0)
    elif edge_idx == 1:
        return (1, 0.5, 0)
    elif edge_idx == 2:
        return (0.5, 1, 0)
    elif edge_idx == 3:
        return (0, 0.5, 0)
    elif edge_idx == 4:
        return (0.5, 0, -1)
    elif edge_idx == 5:
        return (1, 0.5, -1)
    elif edge_idx == 6:
        return (0.5, 1, -1)
    elif edge_idx == 7:
        return (0, 0.5, -1)
    elif edge_idx == 8:
        return (0, 0, -0.5)
    elif edge_idx == 9:
        return (1, 0, -0.5)
    elif edge_idx == 10:
        return (1, 1, -0.5)
    elif edge_idx == 11:
        return (0, 1, -0.5)
    
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
                binary_0 = int(voxel[i+1][j][k])
                binary_1 = int(voxel[i+1][j+1][k])
                binary_2 = int(voxel[i][j][k])
                binary_3 = int(voxel[i][j+1][k])
                binary_4 = int(voxel[i+1][j][k+1])
                binary_5 = int(voxel[i+1][j+1][k+1])
                binary_6 = int(voxel[i][j][k+1])
                binary_7 = int(voxel[i][j+1][k+1])

                bit_encoding = [binary_7, binary_6, binary_5, binary_4, binary_3, binary_2, binary_1, binary_0]
                
                # convert to number
                lookup_idx = np.packbits(bit_encoding)[0]
                edges = get_edges(lookup_idx)

                if len(edges) == 0:
                    continue

                ########### DRAW MESH ###########

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

    from load_voxels import *

    example = create_dummy_voxels()
    cubes = marching_cubes_naive(example)

    plot_mesh(cubes)

    # # save to stl
    # cubes.save('cube.stl')