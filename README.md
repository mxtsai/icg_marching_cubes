# Interactive Computer Graphics - Marching Cubes Implementation

This repository contains the code implementation of Marching Cubes. 

### Libraries

In this repo, I've decided to use Numpy-STL to construct the mesh. Please install numpy-stl to run the code.
```
pip install numpy-stl
```

It is possible to render the mesh using Matplotlib, but I suggest rendering with Blender for larger meshed (larger than 64x64x64).
### How to Use
```
# clone the repository
$ git clone https://github.com/mxtsai/icg_marching_cubes.git

# Go into the repository
$ cd icg_marching_cubes

# run the code
$ python --input "./data/lower" --output "output.stl" --threshold 100 --gaps 5
```
Flags:
* `--input` Path to input image data
* `--output` Path to output STL file
* `--threshold` Threshold for vertex binarization
* `--gaps` Gaps between 2D images


### About
The mesh will be saved as an 'STL' file. This file can be loaded in Blender for better visualization.

### Implementation
I've currently implemented 2 versions of the Marching Cubes algorithm. The first is a naive version that does not take into account any of the difference in values between points. This means that all the vertices will be added in the center point (`alpha=0.5`) between two vertices in the cube. The code is implemented in `marching_cubes.py`.

The second version is an improved version that takes into accound the difference in values of the vertices, and the edge is interpolated using those values. This verison is implemented in `marching_cubes_interp.py`.


### Data
I've downloaded on of the files named `lower` given by Prof. Ouyang. We can try the same code on other data provided by Prof. Ouyang or other data that we can find online.
