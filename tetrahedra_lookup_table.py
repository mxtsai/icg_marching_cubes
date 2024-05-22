
def edge_to_vertex(edge_idx):
    "works for each tetrahedra"
    vertex_mapping = [
        [0, 1],
        [1, 2],
        [2, 3],
        [0, 2],
        [1, 3],
        [0, 3]
    ]
    return vertex_mapping[edge_idx]


def edge_idx_to_unit_tetrahedra_mapping(edge_idx, tetra_idx, alpha=0.5):
    "maps the edge index to a unit tetrahedra coordinate"

    assert edge_idx in list(range(6)), f"{edge_idx} out of range 0-5"
    assert tetra_idx in list(range(6)), f"tetra_idx {tetra_idx} must be in range 0-5"

    if edge_idx == 0:

        if tetra_idx in [0, 3]:
            return (0, 0, alpha)
        elif tetra_idx in [1, 2]:
            return (alpha, 0, 0)
        elif tetra_idx in [4, 5]:
            return (0, alpha, 0)
        
    elif edge_idx == 1:

        if tetra_idx == 0:
            return (alpha, 0, 1)
        elif tetra_idx == 1:
            return (1, 0, alpha)
        elif tetra_idx == 2:
            return (1, alpha, 0)
        elif tetra_idx == 3:
            return (0, alpha, 1)
        elif tetra_idx == 4:
            return (0, 1, alpha)
        elif tetra_idx == 5:
            return (alpha, 1, 0)
    
    elif edge_idx == 2:

        if tetra_idx in [0, 1]:
            return (1, alpha, 1)
        if tetra_idx in [2, 5]:
            return (1, 1, alpha)
        elif tetra_idx in [3, 4]:
            return (alpha, 1, 1)

    elif edge_idx == 3:

        if tetra_idx in [0, 1]:
            # z = x function, y = 0
            return (alpha, 0, alpha)
        elif tetra_idx in [2, 5]:
            # z = 0, y = x 
            return (alpha, alpha, 0)
        elif tetra_idx in [3, 4]:
            # x = 0, z = y
            return (0, alpha, alpha)

    elif edge_idx == 4:

        if tetra_idx in [0, 3]:
            # y = x function, z = 1
            return (alpha, alpha, 1)
        elif tetra_idx in [1, 2]:
            # x = 1, z = y
            return (1, alpha, alpha)
        elif tetra_idx in [4, 5]:
            # y = 1, z = x
            return (alpha, 1, alpha)
        
    elif edge_idx == 5:
        # y = x, z = x function
        return (alpha, alpha, alpha)

def binary_to_base10(binary_list):
    "converts a binary list to base10"
    return int("".join([str(bit) for bit in binary_list]), 2)

def get_edge(idx):
    """idx is the base10 value of the 4 edge binaries
    Checked for all tetrahedras
    """

    edges_list = [
        [],                 # 0000, 0
        [0, 5, 3],          # 0001, 1
        [0, 1, 4],          # 0010, 2
        # [4, 1, 3, 4, 5, 3], # 0011, 3
        [1, 5, 4, 1, 5, 3], # 0011, 3
        [1, 2, 3],          # 0100, 4
        [0, 2, 1, 0, 2, 5], # 0101, 5
        [0, 2, 4, 0, 2, 3], # 0110, 6
        [4, 5, 2],          # 0111, 7
        [4, 5, 2],          # 1000, 8
        [0, 2, 4, 0, 2, 3], # 1001, 9
        [0, 2, 1, 0, 2, 5], # 1010, 10
        [1, 2, 3],          # 1011, 11
        [1, 5, 4, 1, 5, 3], # 1100, 12
        [0, 1, 4],          # 1101, 13
        [0, 5, 3],          # 1110, 14
        [],                 # 1111, 15
    ]

    edge_set = edges_list[idx]

    # divide it up by 3
    edge_triples = [ edge_set[i:i+3] for i in range(0, len(edge_set), 3) ]

    return edge_triples


# import numpy as np

# from stl import mesh

# unit_tetrahedra = [
#     [(0, 0, 0), (0, 0, 1), (1, 0, 1)],
#     [(0, 0, 1), (1, 0, 1), (1, 1, 1)],
#     [(0, 0, 0), (1, 0, 1), (1, 1, 1)],
#     [(0, 0, 0), (0, 0, 1), (1, 1, 1)]
# ]

# rotate = math.pi

# final_mesh = mesh.Mesh(np.zeros(len(unit_tetrahedra), dtype=mesh.Mesh.dtype))
# for triangle_i, triangle in enumerate(unit_tetrahedra):
#     final_mesh.vectors[triangle_i][:] = np.array(triangle)

# from myplot import plot_mesh

# plot_mesh(final_mesh)


# ############# Test Unit Tetrahedra Mapping #############
# vertices = np.array([-1, -1, 1, 0.1])    # vertex [0, 1, 2, 3]
# threshold = 0

# bit_encoding = (vertices > threshold).astype(int)[::-1]

# lookup_idx = binary_to_base10(bit_encoding)
# print(lookup_idx)
# edges = get_edge(lookup_idx)

# print(edges)

# plot_vertices = []
# for triangle in edges:
#     tri_coordinates = []
#     for edge in triangle:

#         # compute the start and end point
#         start_vertex_idx, end_vertex_idx = edge_to_vertex(edge)

#         # get the values of the start and end vertex points
#         start_val = vertices[start_vertex_idx]
#         end_val = vertices[end_vertex_idx]

#         # subtract by the threshold (to enable crossing)
#         start_val -= threshold
#         end_val -= threshold

#         # compute the interpolated point
#         alpha = start_val/(start_val - end_val)
#         print(f"Edge: {edge} - Alpha: {alpha}")

#         edge_coordinates = edge_idx_to_unit_tetrahedra_mapping(edge, alpha=alpha)
#         tri_coordinates.append(edge_coordinates)
    
#     plot_vertices.append(tri_coordinates)

# final_mesh = mesh.Mesh(np.zeros(len(plot_vertices), dtype=mesh.Mesh.dtype))
# for triangle_i, triangle in enumerate(plot_vertices):
#     final_mesh.vectors[triangle_i][:] = np.array(triangle)

# from myplot import plot_mesh

# plot_mesh(final_mesh)