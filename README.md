# Interactive Computer Graphics - Marching Cubes Implementation

This repository contains the code implementation of Marching Cubes. 

### Libraries

In this repo, I've decided to use Numpy-STL to construct the mesh. Please install numpy-stl to run the code.
```
pip install numpy-stl
```

It is possible to render the mesh using Matplotlib, but I suggest rendering with Blender for larger meshed (larger than 64x64x64).


### About
The mesh will be saved as an 'STL' file. This file can be loaded in Blender for better visualization.

### Implementation
I've currently implemented 2 versions of the Marching Cubes algorithm. The first is a naive version that does not take into account any of the difference in values between points. This means that all the vertices will be added in the center point (`alpha=0.5`) between two vertices in the cube. The code is implemented in `marching_cubes.py`.

The second version is an improved version that takes into accound the difference in values of the vertices, and the edge is interpolated using those values. This verison is implemented in `marching_cubes_interp.py`.


### Data
I've downloaded on of the files named `lower` given by Prof. Ouyang. We can try the same code on other data provided by Prof. Ouyang or other data that we can find online.