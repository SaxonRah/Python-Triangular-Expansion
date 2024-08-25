# Python-Triangular-Expansion
Messing around with TEA (Triangular Expansion Algorithm) from the paper "Efficient Computation of Visibility Polygons".

I'm sure a bunch of these examples have logical errors and poorly implemented functions. None of these actually implement the paper 1 to 1. The closest is probably Basic TEA 2, but this doesn't do a number of things.

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
