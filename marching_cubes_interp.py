"""
This is an implementation of the Marching Cubes algorithm with interpolation.
I'll use the same principles as in the 'marching_cubes.py' file, but I'll add
interpolation to the vertices of the triangles.

For this general case, we assume points inside the object to be positive (+) > 0
and points outside the object to be negative (-) < 0. The location for where the
edge crosses the surface (0 value) is calculated by linear interpolation.
"""

import numpy as np
import argparse
from stl import mesh
from mc_lookup_table import get_edges, edge_to_vertex, edge_idx_to_unit_square_mapping


def compute_unit_vertices(edge_set, neighbors, threshold):
    """computes the unit vertices (may contain multiple) given the edge set and neighbor values"""

    edge_set_coordinates = []
    for triangle_edges in edge_set:
        triangle_coordinates = []
        for edge in triangle_edges:   # edge is the index for which edge to add a point to
            
            # compute the start and end point
            start_vertex_idx, end_vertex_idx = edge_to_vertex(edge)

            # get the values of the start and end vertex points
            start_val = neighbors[start_vertex_idx]
            end_val = neighbors[end_vertex_idx]

            # subtract by the threshold (to enable crossing)
            start_val -= threshold
            end_val -= threshold

            # compute the interpolated point
            alpha = start_val/(start_val - end_val)

            # compute the (x, y, z) coordinates based on the edge and the alpha value
            xyz_coordinate = edge_idx_to_unit_square_mapping(edge, alpha)

            # add to triangle coordinates
            triangle_coordinates.append(xyz_coordinate)
        
        # add triangle coordinates of v0, v1, v2 to edge set (may have more than one triange)
        edge_set_coordinates.append(triangle_coordinates)

    return edge_set_coordinates

def apply_translation(triangle, delta_x, delta_y, delta_z):
    return [(x + delta_x, y + delta_y, z + delta_z) for x, y, z in triangle]

def marching_cubes_iterpolation(voxel, threshold=0.0):

    output_dim = np.array(voxel.shape) - 1      # compute the output dimension

    vector_list = []

    # assume i, j, k
    for i in range(output_dim[0]):
        for j in range(output_dim[1]):
            for k in range(output_dim[2]):

                # compute the edge encoding

                # follow ordering from 0 to 7 of the vertex layout
                neighbors = np.array([voxel[i+1][j][k], voxel[i+1][j+1][k], voxel[i][j][k], voxel[i][j+1][k],
                                voxel[i+1][j][k+1], voxel[i+1][j+1][k+1], voxel[i][j][k+1], voxel[i][j+1][k+1]])
                
                # get the binary encoding (need to reverse so order is from 7 -> 0)
                bit_encoding = (neighbors > threshold).astype(int)[::-1]

                # convert to base 10 number
                lookup_idx = np.packbits(bit_encoding)[0]
                edges = get_edges(lookup_idx)

                if len(edges) == 0:
                    continue    # no triangles to build

                # compute unit vertices
                unit_square_coordinates = compute_unit_vertices(edges, neighbors, threshold)

                # apply translation
                delta_x = j
                delta_y = output_dim[0] - i - 1
                delta_z = -k
                translated_coordinates = [apply_translation(triangle, delta_x, delta_y, delta_z) for triangle in unit_square_coordinates]

                # add to vector list
                vector_list.extend(translated_coordinates)

    final_mesh = mesh.Mesh(np.zeros(len(vector_list), dtype=mesh.Mesh.dtype))
    for triangle_i, triangle in enumerate(vector_list):
        final_mesh.vectors[triangle_i][:] = np.array(triangle)

    # # let's translate the mesh to the origin
    # center_of_mass = final_mesh.get_mass_properties()[1]
    # final_mesh.x -= center_of_mass[0]
    # final_mesh.y -= center_of_mass[1]
    # final_mesh.z -= center_of_mass[2]

    return final_mesh

if __name__ == "__main__":

    from myplot import plot_mesh
    from load_voxels import *
    import time

    # example = create_sphere_voxels(space_val=-1, object_val=5)
    parser = argparse.ArgumentParser(description="Marching Cubes")
    parser.add_argument("--input", type=str, help="Path to input voxel data", default="./data/lower")
    parser.add_argument("--output", type=str, help="Path to output STL file", default="output.stl")
    parser.add_argument("--threshold", type=float, help="Threshold for binarization", default=100)
    parser.add_argument("--gaps", type=int, help="Gaps between images", default=1)
    args = parser.parse_args()
    # example = load_ct_folder(args.input)
    # example = np.ones((3, 3, 3))*-1
    # example[1, 1, 1] = 1
    example = load_ct_folder_gaps(args.input, args.gaps)
    start_time = time.time()
    cubes = marching_cubes_iterpolation(example, threshold=args.threshold)
    print(f"Marching Cube took: {time.time() - start_time} seconds")

    # to plot the mesh (suggested for mesh under 64x64x64)
    # plot_mesh(cubes)

    # save to stl (suggested for mesh larger than 64x64x64)
    cubes.save(args.output)

