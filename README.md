# Python-Triangular-Expansion
Messing around with TEA (Triangular Expansion Algorithm) from the paper "Efficient Computation of Visibility Polygons".

I'm sure a bunch of these examples have logical errors and poorly implemented functions. None of these actually implement the paper 1 to 1. The closest is probably Basic TEA 2, but this doesn't do a number of things. I've added a few additions in some other files, Basic_TEA_2_with_CDT.py, Basic_TEA_3.py, and Basic_TEA_3_Performance.py. Basic_TEA_3_Performance is now the closest and best performance (based on feel, no testing was done)

Some of the ideas in other files could be combined with others like for example combining Simplified TEA Visibility and Basic TEA 3 Performance. 

I've also implemented d-TEA (Distance-constrained Triangular Expansion Algorithm) from the paper "Optimizing Mesh to Improve the Triangular Expansion Algorithm for Computing Visibility Regions" in the file "Randomized_dTEA_with_Holes.py" and "Randomized_dTEA_with_Holes_2.py"


# Randomized dTEA with Holes
![Randomized dTEA with Holes](https://github.com/SaxonRah/Python-Triangular-Expansion/blob/main/images/Randomized_dTEA_with_Holes.png)

# Randomized dTEA with Holes 2
![Randomized dTEA with Holes 2](https://github.com/SaxonRah/Python-Triangular-Expansion/blob/main/images/Randomized_dTEA_with_Holes_2.png)

# Basic Grid TEA
![Basic Grid TEA](https://github.com/SaxonRah/Python-Triangular-Expansion/blob/main/images/BasicGridTEA.png)

# Basic Grid TEA 2
![Basic Grid TEA 2](https://github.com/SaxonRah/Python-Triangular-Expansion/blob/main/images/BasicGridTEA2.png)

# Basic TEA
![Basic TEA](https://github.com/SaxonRah/Python-Triangular-Expansion/blob/main/images/Basic_TEA.png)

# Basic TEA 2
![Basic TEA 2](https://github.com/SaxonRah/Python-Triangular-Expansion/blob/main/images/Basic_TEA_2.png)

## Problems with Basic TEA 2
 - Preprocessing with Constrained Delaunay Triangulation
   - In the TEA paper, the initial preprocessing step involves using Constrained Delaunay Triangulation (CDT) instead of a simple Delaunay triangulation. This ensures that the triangulation respects the boundaries of obstacles and the grid.
   - Replace the Delaunay triangulation in triangulate_grid with CDT, which also respects obstacle boundaries.
 - Recursive Visibility Expansion
   - The paper describes a recursive method for expanding the visible area from the observer's position through the edges of the current triangle. This recursion must properly handle the visibility cone restricted by the boundary of the polygon or other obstacles.
   - Implement a recursive function that, given a triangle and an observer's position, expands visibility by checking neighboring triangles while considering visibility constraints.
 - Handle Visibility Polygons with Antennae
   - The TEA paper mentions that the visibility polygon might include antennae (long, thin regions visible from the observer). Ensure that the algorithm can detect and correctly represent these cases.
   - Modify the visibility check to include cases where multiple vertices are collinear with the observer and consider these as potential antennae.
 - Efficiency Improvements
   - The paper emphasizes efficiency, especially in handling large and complex grids. One way to enhance efficiency is to avoid redundant checks by marking triangles that have already been processed.
   - Add a mechanism to skip triangles that have already been fully processed during the recursive expansion.
 - Output Sensitivity
   - Ensure the implementation is output-sensitive, meaning that it processes only the triangles that contribute to the visible region, thereby improving runtime.
   - Implement checks to avoid unnecessary processing of triangles that do not contribute to the final visibility polygon.
 - Visualization of Visibility Cones.
   - The paper's examples visualize the expanding visibility cone as it moves from one triangle to the next. Implementing this in the visualization could help in debugging and understanding the algorithm's behavior.
   - Add a function to draw the visibility cone as it expands through triangles.
 - Handling Degenerate Cases
   - The TEA algorithm in the paper handles degenerate cases such as collinear points or overlapping edges.
   - Add edge cases handling in the triangulation and visibility checks to account for collinear points and overlapping triangles.
 - Benchmarks and Performance Testing
   - The paper discusses various scenarios (like the Norway and cathedral examples) to benchmark the algorithm's performance. Implement similar test scenarios in the code to evaluate and optimize performance.
   - Create different loadable grid configurations and measure the performance of the implementation vs other scenarios.
  
# Basic TEA 2 with CDT
![Basic TEA 2 with CDT](https://github.com/SaxonRah/Python-Triangular-Expansion/blob/main/images/Basic_TEA_2_with_CDT.png)
## This is an example of CDT using Basic_TEA_2.py as a base.

# Basic TEA 3
![Basic TEA 3](https://github.com/SaxonRah/Python-Triangular-Expansion/blob/main/images/Basic_TEA_3.png)
## This is an example of handling the visibility of polygons with antennae using Basic_TEA_2_with_CDT.py as a base.

# Basic TEA 3 Performance
![Basic TEA 3](https://github.com/SaxonRah/Python-Triangular-Expansion/blob/main/images/Basic_TEA_3_Performance.png)
## This is an example of better performance with using Basic_TEA_3.py as a base.

# Simplified TEA Visibility
![Simplified TEA Visibility](https://github.com/SaxonRah/Python-Triangular-Expansion/blob/main/images/Simplified_TEA_Visibility.png)

# Simplified TEA Visibility 2
![Simplified TEA Visibility 2](https://github.com/SaxonRah/Python-Triangular-Expansion/blob/main/images/Simplified_TEA_Visibility_2.png)

# Grid Triangulation
![Grid Triangulation](https://github.com/SaxonRah/Python-Triangular-Expansion/blob/main/images/Grid_Triangulation.png)

# Raycast Grid Visibility
![Raycast_Grid_Visibility](https://github.com/SaxonRah/Python-Triangular-Expansion/blob/main/images/Raycast_Grid_Visibility.png)

# Raycast Grid Visibility 2
![Raycast_Grid_Visibility 2](https://github.com/SaxonRah/Python-Triangular-Expansion/blob/main/images/Raycast_Grid_Visibility_2.png)

# Raycast Grid Visibility 3
![Raycast_Grid_Visibility 3](https://github.com/SaxonRah/Python-Triangular-Expansion/blob/main/images/Raycast_Grid_Visibility_3.png)

# Simple Triangulation
![Simple Triangulation](https://github.com/SaxonRah/Python-Triangular-Expansion/blob/main/images/Simple_Triangulation.png)
